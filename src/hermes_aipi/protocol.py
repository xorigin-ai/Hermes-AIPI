from __future__ import annotations

import struct
import time
from dataclasses import dataclass
from enum import IntEnum

MAGIC = 0x4845524D
VERSION = 1
HEADER = struct.Struct("!IBBHII")


class Direction(IntEnum):
    MIC_TO_HERMES = 1
    HERMES_TO_SPEAKER = 2


@dataclass(frozen=True)
class AudioFrame:
    direction: Direction
    stream_id: int
    sequence: int
    timestamp_ms: int
    pcm: bytes


def pack_audio(pcm: bytes, direction: Direction, stream_id: int, sequence: int, timestamp_ms: int | None = None) -> bytes:
    if timestamp_ms is None:
        timestamp_ms = int(time.time() * 1000) & 0xFFFFFFFF
    return HEADER.pack(MAGIC, VERSION, int(direction), stream_id & 0xFFFF, sequence & 0xFFFFFFFF, timestamp_ms & 0xFFFFFFFF) + pcm


def unpack_audio(data: bytes) -> AudioFrame:
    if len(data) < HEADER.size:
        raise ValueError("short HERM frame")
    magic, version, direction, stream_id, sequence, timestamp_ms = HEADER.unpack(data[:HEADER.size])
    if magic != MAGIC:
        raise ValueError("invalid HERM magic")
    if version != VERSION:
        raise ValueError(f"unsupported HERM version {version}")
    return AudioFrame(Direction(direction), stream_id, sequence, timestamp_ms, data[HEADER.size:])
