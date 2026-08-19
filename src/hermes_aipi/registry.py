from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


@dataclass
class DeviceRecord:
    device_id: str
    name: str
    default_bot_id: str


class DeviceRegistry:
    def __init__(self, path: Path):
        self.path = path
        self.devices: Dict[str, DeviceRecord] = {}

    def load(self) -> None:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.devices = {
            item["device_id"]: DeviceRecord(**item)
            for item in data.get("devices", [])
        }

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"devices": [asdict(d) for d in self.devices.values()]}
        self.path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def get(self, device_id: str) -> DeviceRecord:
        return self.devices[device_id]

    def assign(self, device_id: str, bot_id: str) -> DeviceRecord:
        record = self.get(device_id)
        record.default_bot_id = bot_id
        self.save()
        return record

    def list(self) -> List[DeviceRecord]:
        return list(self.devices.values())
