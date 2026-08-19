from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Awaitable, Callable, Dict, Optional

import websockets
from websockets.server import ServerConnection

from .protocol import AudioFrame, Direction, pack_audio, unpack_audio
from .registry import DeviceRegistry

log = logging.getLogger("hermes_aipi.bridge")

AudioHandler = Callable[[str, str, AudioFrame], Awaitable[None]]
EventHandler = Callable[[str, str, dict], Awaitable[None]]


@dataclass
class ConnectedDevice:
    device_id: str
    bot_id: str
    websocket: ServerConnection
    name: str
    firmware_version: str = "unknown"
    tx_sequence: int = 0
    stream_id: int = 1


class LocalBridge:
    def __init__(self, registry: DeviceRegistry, host: str = "0.0.0.0", port: int = 8765):
        self.registry = registry
        self.host = host
        self.port = port
        self.devices: Dict[str, ConnectedDevice] = {}
        self.on_audio: Optional[AudioHandler] = None
        self.on_event: Optional[EventHandler] = None
        self._server = None

    async def start(self) -> None:
        self._server = await websockets.serve(self._client, self.host, self.port, max_size=2 * 1024 * 1024)
        log.info("Hermes-AIPI listening on ws://%s:%s", self.host, self.port)

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    async def _client(self, websocket: ServerConnection) -> None:
        first = await asyncio.wait_for(websocket.recv(), timeout=10)
        if not isinstance(first, str):
            await websocket.close(code=1008, reason="device.hello required")
            return
        hello = json.loads(first)
        if hello.get("type") != "device.hello" or not hello.get("device_id"):
            await websocket.close(code=1008, reason="invalid device.hello")
            return

        device_id = hello["device_id"]
        if device_id not in self.registry.devices:
            await websocket.close(code=1008, reason="unknown device_id")
            return

        record = self.registry.get(device_id)
        dev = ConnectedDevice(
            device_id=device_id,
            bot_id=record.default_bot_id,
            websocket=websocket,
            name=record.name,
            firmware_version=hello.get("firmware_version", "unknown"),
        )
        self.devices[device_id] = dev
        await websocket.send(json.dumps({
            "type": "device.welcome",
            "protocol_version": 1,
            "device_id": device_id,
            "assigned_bot_id": dev.bot_id,
            "audio": {"codec": "pcm_s16le", "sample_rate": 16000, "channels": 1, "frame_ms": 20},
        }))
        log.info("%s connected -> Bot %s", device_id, dev.bot_id)

        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    frame = unpack_audio(message)
                    if frame.direction is Direction.MIC_TO_HERMES and self.on_audio:
                        await self.on_audio(device_id, dev.bot_id, frame)
                else:
                    event = json.loads(message)
                    if event.get("type") == "device.button" and event.get("button") == "ptt":
                        await self.cancel_output(device_id, "barge_in")
                    if self.on_event:
                        await self.on_event(device_id, dev.bot_id, event)
        finally:
            self.devices.pop(device_id, None)
            log.info("%s disconnected", device_id)

    async def assign_bot(self, device_id: str, bot_id: str) -> None:
        self.registry.assign(device_id, bot_id)
        if device_id in self.devices:
            self.devices[device_id].bot_id = bot_id
            await self.send_json(device_id, {"type": "bot.assignment", "bot_id": bot_id})

    async def send_json(self, device_id: str, payload: dict) -> None:
        await self.devices[device_id].websocket.send(json.dumps(payload))

    async def send_audio(self, device_id: str, pcm: bytes) -> None:
        dev = self.devices[device_id]
        dev.tx_sequence += 1
        await dev.websocket.send(pack_audio(pcm, Direction.HERMES_TO_SPEAKER, dev.stream_id, dev.tx_sequence))

    async def set_state(self, device_id: str, state: str, bot_name: str | None = None) -> None:
        await self.send_json(device_id, {"type": "display.state", "state": state, "bot_name": bot_name})

    async def cancel_output(self, device_id: str, reason: str) -> None:
        dev = self.devices.get(device_id)
        if not dev:
            return
        dev.stream_id = (dev.stream_id + 1) & 0xFFFF
        await self.send_json(device_id, {"type": "conversation.cancel", "reason": reason, "new_stream_id": dev.stream_id})
