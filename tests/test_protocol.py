from hermes_aipi.protocol import Direction, pack_audio, unpack_audio


def test_herm_roundtrip():
    pcm = b"\x01\x02" * 320
    raw = pack_audio(pcm, Direction.MIC_TO_HERMES, stream_id=7, sequence=42, timestamp_ms=1234)
    frame = unpack_audio(raw)
    assert frame.direction is Direction.MIC_TO_HERMES
    assert frame.stream_id == 7
    assert frame.sequence == 42
    assert frame.timestamp_ms == 1234
    assert frame.pcm == pcm


def test_header_is_16_bytes():
    raw = pack_audio(b"", Direction.HERMES_TO_SPEAKER, stream_id=1, sequence=1, timestamp_ms=1)
    assert len(raw) == 16
