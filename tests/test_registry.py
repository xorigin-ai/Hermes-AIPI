import json
from pathlib import Path

from hermes_aipi.registry import DeviceRegistry


def test_assignment_persists(tmp_path: Path):
    path = tmp_path / "devices.json"
    path.write_text(json.dumps({"devices": [{"device_id": "aipi-01", "name": "AI Pi 01", "default_bot_id": "general"}]}), encoding="utf-8")
    reg = DeviceRegistry(path)
    reg.load()
    reg.assign("aipi-01", "research")

    reg2 = DeviceRegistry(path)
    reg2.load()
    assert reg2.get("aipi-01").default_bot_id == "research"
