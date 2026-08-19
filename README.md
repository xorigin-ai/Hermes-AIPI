# Hermes-AIPI

Local Windows 11 proof of concept for **Hermes Desktop Bot Mode** controlling five AI Pi Lite endpoints over the local LAN.

## POC thesis

A fresh Windows 11 Hermes Desktop install can create persistent named Bots, assign them to physical AI Pi Lite endpoints, route device/voice events into those Bots, let Bots use existing Hermes apps, and allow Bot-to-Bot collaboration without any VPS, O-ai.cloud, or remote MCP dependency.

**Architectural invariant:** the Bot is the agent; the AI Pi Lite is a physical endpoint.

## Scope lock

Included:

- Windows 11 Hermes dev box
- current Hermes Desktop Bot Mode
- five AI Pi Lite devices on one LAN
- persistent Hermes Bot profiles
- persistent device-to-Bot assignment
- HERM 16-byte PCM framing
- local WebSocket endpoint bridge
- speaker/microphone routing hooks
- display/state channel
- telemetry/events and barge-in
- existing Hermes-compatible apps
- Bot-to-Bot delegation

Explicitly excluded from this POC:

- VPS deployment
- O-ai.cloud
- remote/shared MCP infrastructure
- cloud control plane
- distributed multi-site orchestration

## Current implementation

This branch now includes a runnable Windows-local bridge scaffold rather than architecture documents only:

```text
src/hermes_aipi/
  bridge.py       AI Pi Lite WebSocket connections and Bot routing
  protocol.py     canonical HERM 16-byte audio framing
  registry.py     persistent device_id -> Hermes Bot mapping
  main.py         local runtime entrypoint

config/
  devices.example.json

scripts/
  bootstrap-windows.ps1
  run-bridge.ps1

tests/
  test_protocol.py
  test_registry.py

docs/
  ARCHITECTURE.md
  POC_CONTRACT.md
  DEVICE_BOT_MODEL.md
  SOURCE_PROVENANCE.md
  HERMES_HANDOFF.md
```

## Fresh Windows 11 handoff

Clone this repository/branch onto the fresh Hermes dev box, then run PowerShell:

```powershell
.\scripts\bootstrap-windows.ps1
```

The bootstrap creates `.venv`, installs the local package and test dependencies, creates `runtime/config/devices.json`, and runs the unit tests.

Start the device bridge with:

```powershell
.\scripts\run-bridge.ps1
```

Then give Hermes **`docs/HERMES_HANDOFF.md`** as the controlling implementation brief. Hermes should inspect the current installed/current Hermes Desktop Bot Mode source/API before wiring the bridge to profiles and sessions; do not guess undocumented interfaces.

## Initial device map

```text
aipi-01 -> general
aipi-02 -> research
aipi-03 -> coding
aipi-04 -> operations
aipi-05 -> specialist
```

These are initial profile identifiers and can be updated to the actual persistent Bot profile IDs/names created on the fresh box without reflashing devices.

## Source donors

- `xorigin-ai/Hermes-AIPI-lite` — HERM framing, hardware bridge, telemetry/control and Hermes integration patterns
- `xorigin-ai/Buddy/hermes-esp32-face/firmware/xiaozhi` — ESP32-S3 firmware reference
- `xorigin-ai/Buddy/buddy_gibbertalk_ai_studio_handoff` — optional voice/avatar/protocol references
- current Nous Research Hermes Desktop — authoritative Bot Mode/profile behavior

See `docs/SOURCE_PROVENANCE.md`. Preserve donor licenses and do not blindly import Linux/VPS assumptions.

## POC acceptance criteria

1. Fresh Hermes Desktop installation on Windows 11.
2. Five named persistent Bots exist with distinct profiles.
3. Five AI Pi Lite devices pair locally and survive restart.
4. Each device can be assigned/reassigned to a Bot without reflashing.
5. Mic audio reaches the assigned Hermes Bot and response audio returns to the originating endpoint.
6. Hermes controls display/state, LED/volume where supported, telemetry, and barge-in.
7. At least one Bot invokes an existing Hermes-compatible app.
8. At least one Bot delegates to another Bot and consumes the result.
9. Reboot preserves Bot profiles, device identities, and assignments.
10. Core demonstration works with WAN disconnected once required local assets are installed.

## Important status boundary

The repository is **ready to hand to Hermes for implementation on the actual Windows 11 dev box**, but the physical-device POC is not yet proven. Completion requires the real Hermes Bot/session adapter and AI Pi Lite firmware to be connected and validated against `docs/POC_CONTRACT.md`.
