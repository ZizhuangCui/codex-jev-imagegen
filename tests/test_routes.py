"""Capability routing tests. Fixtures represent tools; no providers are called."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/jev-imagegen/scripts/route.py"
spec = importlib.util.spec_from_file_location("route", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def tool(name="fixture.generate", models=None, operations=None, limit=2):
    return {"name": name, "models": models or [], "operations": operations or ["generate", "edit"],
            "max_references": limit, "evidence": "Offline fixture, not a real connected provider"}


class Routes(unittest.TestCase):
    def test_registered_versions_and_aliases(self):
        seen = set()
        for model in module.catalog():
            inventory = {"tools": [tool(models=[model["id"]])]}
            for name in [model["id"], model["label"], *model["aliases"]]:
                result = module.route(name, inventory, "edit", 1)
                self.assertEqual(result["status"], "handoff")
                self.assertEqual(result["model"], model["id"])
                self.assertFalse(result["executed"])
            self.assertNotIn(model["id"], seen)
            seen.add(model["id"])
        self.assertEqual(len(seen), 15)

    def test_builtin_does_not_satisfy_specific_model(self):
        inventory = {"tools": [tool("image_gen")]}
        self.assertIsNone(module.route("builtin", inventory)["model"])
        self.assertEqual(module.route("gen2", inventory)["reason"], "no_compatible_tool")
        inventory["tools"][0]["models"] = ["gpt-image-2"]
        with self.assertRaises(ValueError):
            module.route("gen2", inventory)

    def test_unavailable_and_unknown_models_do_not_fallback(self):
        self.assertEqual(module.route("Nano Banana Pro", {"tools": []})["reason"], "no_compatible_tool")
        result = module.route("gemini-3-pro-image-preview", {"tools": []})
        self.assertEqual(result["reason"], "unknown_model")
        self.assertEqual(result["requested_model"], "gemini-3-pro-image-preview")

    def test_ambiguous_versions_and_tools(self):
        result = module.route("image gen 2.5", {"tools": []})
        self.assertEqual(result["reason"], "choose_version")
        self.assertEqual(len(result["candidates"]), 2)
        inventory = {"tools": [tool(name=n, models=["gpt-image-1"]) for n in ["fixture.a", "fixture.b"]]}
        self.assertEqual(module.route("gen1", inventory)["reason"], "choose_tool")
        self.assertEqual(module.route("gen1", inventory, preferred_tool="fixture.b")["tool"], "fixture.b")

    def test_reference_capacity_and_edit_capability(self):
        inventory = {"tools": [tool(models=["gemini-3-pro-image"], operations=["generate"])]}
        self.assertEqual(module.route("Nano Banana Pro", inventory, "edit", 1)["reason"], "no_compatible_tool")
        self.assertEqual(module.route("Nano Banana Pro", inventory, reference_count=3)["reason"], "no_compatible_tool")
        self.assertEqual(module.route("Nano Banana Pro", inventory, "edit", 0)["reason"], "missing_edit_target")

    def test_malformed_inventory(self):
        for value in [None, {}, {"tools": [None]}, {"tools": [tool(limit=True)]}, {"tools": [tool(), tool()]}]:
            with self.assertRaises(ValueError):
                module.route("builtin", value)

    def test_cli_default_has_no_assumed_tool(self):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT)], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["reason"], "no_compatible_tool")


if __name__ == "__main__":
    unittest.main()
