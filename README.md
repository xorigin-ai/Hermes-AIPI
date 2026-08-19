# Hermes-AIPI

Local Windows 11 proof of concept for **Hermes Desktop Bot Mode** controlling five AI Pi Lite endpoints over the local LAN.

## POC thesis

A fresh Windows 11 Hermes Desktop install can create persistent named Bots, assign them to physical AI Pi Lite endpoints, route voice/device events into those Bots, let Bots use existing Hermes apps, and allow Bot-to-Bot collaboration without any VPS, O-ai.cloud, or remote MCP dependency.

## Scope

- Windows 11 Hermes dev box
- Hermes Desktop with Bot Mode front and center
- Five AI Pi Lite devices on the same LAN
- Hermes-specific AI Pi firmware
- Persistent Bot identities with role, model, memory, skills, and avatar
- Device-to-Bot assignment and reassignment
- Bot-to-Bot communication
- Local device discovery, audio, screen, LED, volume, telemetry, and barge-in
- Reuse of existing Hermes-compatible apps where practical

## Explicitly out of scope for this POC

- VPS deployment
- O-ai.cloud
- Remote/shared MCP infrastructure
- Cloud control plane
- Distributed multi-site orchestration

## Source donors

This repository consolidates and adapts existing work rather than starting from zero:

- `xorigin-ai/Hermes-AIPI-lite` — hardware bridge, HERM framing, device telemetry/control, Hermes integration patterns
- `xorigin-ai/Buddy/hermes-esp32-face` — ESP32/Xiaozhi firmware and display/face references
- `xorigin-ai/Buddy/buddy_gibbertalk_ai_studio_handoff` — voice, avatar/state, and protocol donor references
- Nous Research Hermes Desktop — authoritative Bot Mode/profile behavior

Linux/VPS assumptions from donor projects must not be copied blindly into this Windows-local POC.

## Target topology

```text
Windows 11 Hermes Desktop
        |
        +-- Bot 1
        +-- Bot 2
        +-- Bot 3
        +-- Bot 4
        +-- Bot 5
        |
        +-- Hermes-AIPI local bridge
                |
                +-- AI Pi Lite 01
                +-- AI Pi Lite 02
                +-- AI Pi Lite 03
                +-- AI Pi Lite 04
                +-- AI Pi Lite 05
```

The Bots are the agents. The AI Pi Lite devices are physical Hermes endpoints.

## POC acceptance criteria

1. Fresh Hermes Desktop installation on Windows 11.
2. Five named Bots exist with distinct profiles.
3. Five AI Pi Lite devices pair locally and survive restart.
4. Each device can be assigned to a default Bot and reassigned.
5. Mic audio reaches Hermes and responses return to the correct device.
6. Hermes can control screen, LED, volume, telemetry, and barge-in.
7. At least one Bot invokes an existing Hermes-compatible app.
8. At least one Bot delegates work to another Bot and consumes the result.
9. Reboot preserves Bot profiles, memories, device identities, and assignments.
10. The demo functions with the WAN disconnected after required models/dependencies are locally available.

## Repository layout

```text
docs/
  ARCHITECTURE.md
  POC_CONTRACT.md
  DEVICE_BOT_MODEL.md
  SOURCE_PROVENANCE.md
config/
  devices.example.json
scripts/
  bootstrap-windows.ps1
```

The first milestone is architecture and bootstrap. Runtime bridge and firmware consolidation follow against this contract.
