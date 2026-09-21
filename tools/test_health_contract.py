"""Offline artifact contract checks. NOT a Home Assistant runtime test."""
import json
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]

class HealthContract(unittest.TestCase):
    def setUp(self):
        # JSON is a YAML subset, deliberately used for dependency-free checks.
        self.package = json.loads((ROOT / "home-assistant/decca-health-package.yaml").read_text(encoding="utf-8"))
        self.dashboard = json.loads((ROOT / "home-assistant/decca-health-dashboard.yaml").read_text(encoding="utf-8"))
        self.sensors = self.package["mqtt"]["sensor"]

    def test_fixtures_supply_every_sensor(self):
        for fixture in (ROOT / "home-assistant/fixtures").glob("*.json"):
            data = json.loads(fixture.read_text(encoding="utf-8"))
            for sensor in self.sensors:
                key = re.fullmatch(r"{{ value_json\.([a-z_]+) }}", sensor["value_template"])[1]
                self.assertIn(key, data, (fixture, key))
                if sensor.get("state_class"):
                    self.assertIsInstance(data[key], (int, float))

    def test_dashboard_references_exact_trial_entities(self):
        configured = {s["default_entity_id"] for s in self.sensors}
        self.assertEqual(len(configured), len(self.sensors))
        self.assertEqual(len({s["unique_id"] for s in self.sensors}), len(self.sensors))
        shown = set()
        for card in self.dashboard["views"][0]["cards"]:
            shown.update(card.get("entities", []))
        self.assertEqual(shown, configured)

    def test_stale_and_isolation_contract(self):
        for sensor in self.sensors:
            self.assertEqual(sensor["state_topic"], "decca/trial/health/state")
            self.assertEqual(sensor["availability_topic"], "decca/trial/health/availability")
            self.assertEqual(sensor["expire_after"], 660)
            self.assertGreater(sensor["expire_after"], 2 * 300)
            self.assertNotIn("command_topic", sensor)

    def test_recovery_and_reboot_examples(self):
        read = lambda name: json.loads((ROOT / f"home-assistant/fixtures/{name}.json").read_text(encoding="utf-8"))
        healthy, recovered, rebooted = map(read, ("healthy", "recovered", "rebooted"))
        self.assertGreater(recovered["wifi_disconnects"], healthy["wifi_disconnects"])
        self.assertLess(recovered["min_rssi_dbm"], healthy["min_rssi_dbm"])
        self.assertLess(rebooted["uptime_s"], recovered["uptime_s"])
        self.assertEqual(rebooted["wifi_disconnects"], 0)
        self.assertEqual(rebooted["reset_reason"], "brownout")

class UploadGuard(unittest.TestCase):
    def test_compile_allowed_and_every_upload_target_rejected(self):
        import runpy
        import sys
        import types
        from unittest.mock import patch
        module = types.ModuleType("SCons.Script")
        with patch.dict(sys.modules, {"SCons.Script": module}):
            module.COMMAND_LINE_TARGETS = ["buildprog"]
            runpy.run_path(str(ROOT / "tools/block_trial_upload.py"), init_globals={"Import": lambda name: None})
            for target in ("upload", "uploadfs", "nobuild", "size"):
                module.COMMAND_LINE_TARGETS = [target]
                if "upload" in target:
                    with self.assertRaisesRegex(RuntimeError, "compile-only"):
                        runpy.run_path(str(ROOT / "tools/block_trial_upload.py"), init_globals={"Import": lambda name: None})
                else:
                    runpy.run_path(str(ROOT / "tools/block_trial_upload.py"), init_globals={"Import": lambda name: None})

if __name__ == "__main__":
    unittest.main()
