import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from backup_planner.cli import apply_plan, build_plan, sha256

class BackupPlannerTests(unittest.TestCase):
    def test_create_apply_and_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, destination = root / "source", root / "backup"
            source.mkdir()
            (source / "docs").mkdir()
            original = source / "docs" / "notes.txt"
            original.write_text("important", encoding="utf-8")
            plan = build_plan(source, destination)
            self.assertEqual(len(plan), 1)
            manifest = destination / "manifest.json"
            report = apply_plan(plan, manifest, verify=True)
            copied = destination / "docs" / "notes.txt"
            self.assertEqual(report["copied_files"], 1)
            self.assertEqual(sha256(original), sha256(copied))
            self.assertEqual(build_plan(source, destination), [])

    def test_destination_inside_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            with self.assertRaises(ValueError):
                build_plan(source, source / "backup")

if __name__ == "__main__":
    unittest.main()
