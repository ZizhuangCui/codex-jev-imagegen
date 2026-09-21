#!/usr/bin/env python3
"""Resolve a requested image model against observed Codex tools; never call a provider."""
import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "references/models.json"


def catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["models"]


def normalize(value):
    return " ".join(value.lower().strip().replace("_", " ").split())


def resolve(model):
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be nonempty text")
    name = normalize(model)
    if name in {"builtin", "image_gen", "image gen", "codex", "codex builtin"}:
        return {"id": "builtin", "family": "codex"}
    for item in catalog():
        if name in [normalize(v) for v in [item["id"], item["label"], *item["aliases"]]]:
            return item
    return None


def validate_inventory(inventory):
    if not isinstance(inventory, dict) or set(inventory) != {"tools"} or not isinstance(inventory["tools"], list):
        raise ValueError("Expected tools inventory")
    names = set()
    for tool in inventory["tools"]:
        if not isinstance(tool, dict) or set(tool) != {"name", "models", "operations", "max_references", "evidence"}:
            raise ValueError("Invalid tool record")
        for field in ("name", "evidence"):
            if not isinstance(tool[field], str) or not tool[field].strip():
                raise ValueError("Missing tool identity/evidence")
        if tool["name"] in names:
            raise ValueError("Duplicate tool")
        names.add(tool["name"])
        for field in ("models", "operations"):
            if not isinstance(tool[field], list) or any(not isinstance(v, str) or not v.strip() for v in tool[field]):
                raise ValueError("Invalid tool capabilities")
        if not tool["operations"] or set(tool["operations"]) - {"generate", "edit"}:
            raise ValueError("Invalid operation")
        if type(tool["max_references"]) is not int or tool["max_references"] < 0:
            raise ValueError("Invalid reference capacity")
        if tool["name"] == "image_gen" and tool["models"]:
            raise ValueError("Built-in image_gen has no model selector")
    return inventory["tools"]


def route(model, inventory, operation="generate", reference_count=0, preferred_tool=None):
    tools = validate_inventory(inventory)
    if operation not in {"generate", "edit"} or type(reference_count) is not int or reference_count < 0:
        raise ValueError("Invalid task requirements")
    if operation == "edit" and reference_count == 0:
        return {"status": "blocked", "reason": "missing_edit_target"}
    selected = resolve(model)
    if selected is None:
        candidates = []
        if normalize(model) in {"gen2.5", "image gen 2.5", "gpt-image-2.5", "gpt image 2.5"}:
            candidates = [m["id"] for m in catalog() if m["id"].startswith("gpt-image-2.5-")]
        elif normalize(model) in {"seedream", "nano banana family"}:
            family = "seedream" if normalize(model) == "seedream" else "google"
            candidates = [m["id"] for m in catalog() if m["family"] == family]
        return {"status": "blocked", "reason": "choose_version" if candidates else "unknown_model",
                "requested_model": model, "candidates": candidates}
    matches = [t for t in tools if
               (t["name"] == "image_gen" if selected["id"] == "builtin" else
                t["name"] != "image_gen" and selected["id"] in t["models"])
               and operation in t["operations"] and reference_count <= t["max_references"]
               and (preferred_tool is None or t["name"] == preferred_tool)]
    if len(matches) != 1:
        return {"status": "blocked", "reason": "choose_tool" if matches else "no_compatible_tool",
                "requested_model": model, "model": selected["id"], "tools": [t["name"] for t in matches]}
    return {"status": "handoff", "tool": matches[0]["name"], "requested_model": model,
            "model": None if selected["id"] == "builtin" else selected["id"],
            "family": selected["family"], "operation": operation, "reference_count": reference_count,
            "observed_model": None, "executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--model", default="builtin")
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--operation", choices=("generate", "edit"), default="generate")
    parser.add_argument("--reference-count", type=int, default=0)
    parser.add_argument("--tool")
    args = parser.parse_args()
    try:
        if args.list:
            result = {"models": catalog(), "support": "connected-tool routing; not live validation"}
        else:
            inventory = json.loads(args.inventory.read_text(encoding="utf-8")) if args.inventory else {"tools": []}
            result = route(args.model, inventory, args.operation, args.reference_count, args.tool)
    except (ValueError, TypeError, OSError):
        print(json.dumps({"status": "invalid_input", "reason": "Check inventory schema and task requirements"}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 3 if result.get("status") == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
