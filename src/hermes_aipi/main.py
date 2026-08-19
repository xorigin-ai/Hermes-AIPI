from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path

from .bridge import LocalBridge
from .registry import DeviceRegistry


async def run(registry_path: Path, host: str, port: int) -> None:
    registry = DeviceRegistry(registry_path)
    registry.load()
    bridge = LocalBridge(registry, host=host, port=port)

    async def on_audio(device_id, bot_id, frame):
        logging.getLogger("hermes_aipi.audio").debug(
            "audio %s -> bot=%s seq=%s bytes=%s",
            device_id,
            bot_id,
            frame.sequence,
            len(frame.pcm),
        )

    async def on_event(device_id, bot_id, event):
        logging.getLogger("hermes_aipi.event").info(
            "event %s -> bot=%s type=%s", device_id, bot_id, event.get("type")
        )

    bridge.on_audio = on_audio
    bridge.on_event = on_event
    await bridge.start()
    try:
        await asyncio.Event().wait()
    finally:
        await bridge.stop()


def cli() -> None:
    parser = argparse.ArgumentParser(description="Hermes-AIPI local Windows bridge")
    parser.add_argument("--registry", default="runtime/config/devices.json")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    asyncio.run(run(Path(args.registry), args.host, args.port))


if __name__ == "__main__":
    cli()
