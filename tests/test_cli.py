"""Public installation and command-line checks; no network or credentials."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/jev-imagegen/scripts/decide.py"


class CliChecks(unittest.TestCase):
    def run_helper(self, *args):
        env = os.environ.copy()
        env.pop("TYPESAFE_API_KEY", None)
        return subprocess.run([sys.executable, "-B", str(HELPER), *args], env=env,
                              capture_output=True, text=True, timeout=10)

    def test_request_and_missing_credentials(self):
        args = ["--phase", "plan", "--input", str(ROOT / "examples/generate.json")]
        result = self.run_helper(*args)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "request_only")
        result = self.run_helper(*args, "--mode", "live")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["reason"], "missing_key")

    def test_bad_input_and_uninspected_review(self):
        result = self.run_helper("--phase", "plan", "--input", str(ROOT / "nonexistent-input.json"))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "invalid_input")
        result = self.run_helper("--phase", "review", "--input", str(ROOT / "examples/review.json"), "--mode", "live")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["reason"], "uninspected_output")

    def test_install_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, str(ROOT / "install.py"), "--skills-dir", directory]
            result = subprocess.run(command, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0)
            installed = Path(directory) / "jev-imagegen"
            self.assertTrue((installed / "SKILL.md").is_file())
            marker = installed / "local-note.txt"
            marker.write_text("Preserve local changes")
            result = subprocess.run(command, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(marker.read_text(), "Preserve local changes")


if __name__ == "__main__":
    unittest.main()
