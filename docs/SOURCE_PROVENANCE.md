# Source Provenance

This POC is a consolidation project. Reuse must remain traceable.

## Primary donors

### xorigin-ai/Hermes-AIPI-lite

Role: local bridge/protocol donor.

Relevant material:

- `hardware_bridge.py`
- `main.py`
- `mcp_tools.py`
- `docs/ARCHITECTURE.md`
- `docs/PROTOCOL.md`
- `docs/HERMES_INTEGRATION.md`
- `docs/HARDWARE.md`
- `docs/FLASHING.md`

Adaptation note: this donor is VPS/Linux-first. The POC target is Windows 11 and local-only, so systemd, `/opt/...`, remote MCP, and VPS assumptions are not architectural requirements.

### xorigin-ai/Buddy

Role: firmware, voice, avatar, and protocol reference donor.

Relevant material:

- `hermes-esp32-face/firmware/face`
- `hermes-esp32-face/firmware/xiaozhi`
- `buddy_gibbertalk_ai_studio_handoff`

The Xiaozhi subtree is the main ESP32 firmware reference. Buddy application logic is not automatically part of the endpoint firmware.

### Nous Research Hermes Desktop

Role: authoritative Bot Mode behavior.

Bot Mode/profile semantics must be taken from the current Hermes Desktop implementation/documentation, not recreated from assumptions.

## Reuse policy

1. Prefer adapting proven donor components over rebuilding plumbing.
2. Preserve attribution/license information from source projects.
3. Do not copy incompatible deployment assumptions into the POC.
4. Keep cognition inside Hermes Desktop; endpoint firmware stays thin.
5. Document major migrations and behavioral changes in this file or a dedicated migration note.

## Future donors

Other xorigin-ai applications may be used as proof workloads for Bots, but they are not core runtime dependencies.
