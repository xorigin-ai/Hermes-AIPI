# Architecture

## System boundary

Hermes-AIPI is a local device integration layer for Hermes Desktop. It must not become a competing agent runtime.

```text
+--------------------------------------------------------------+
| Windows 11 Hermes Desktop                                    |
|                                                              |
|  Bot Mode                                                    |
|  +-----------+ +-----------+ +-----------+                   |
|  | Bot A     | | Bot B     | | Bot C     | ...               |
|  | role      | | role      | | role      |                   |
|  | model     | | model     | | model     |                   |
|  | memory    | | memory    | | memory    |                   |
|  | skills    | | skills    | | skills    |                   |
|  +-----+-----+ +-----+-----+ +-----+-----+                   |
|        \             |             /                         |
|         +------------+------------+                          |
|                      |                                       |
|             Hermes-AIPI local bridge                         |
|             +----------------------+                         |
|             | device registry      |                         |
|             | session routing      |                         |
|             | HERM transport       |                         |
|             | audio streams        |                         |
|             | display/LED control  |                         |
|             | telemetry/barge-in   |                         |
|             +----------+-----------+                         |
+------------------------|-------------------------------------+
                         | LAN / Wi-Fi
             +-----------+-----------+-----------+-----------+
             |           |           |           |           |
           Pi-01       Pi-02       Pi-03       Pi-04       Pi-05
```

## Responsibility split

### Hermes Desktop

Owns cognition and orchestration:

- Bot profiles
- models
- memory
- skills
- existing apps/tools
- Bot-to-Bot communication
- user interaction state

### Hermes-AIPI

Owns endpoint integration:

- device discovery and pairing
- persistent device registry
- device-to-Bot mapping
- local transport
- session correlation
- audio routing
- screen/LED/volume control
- telemetry
- barge-in and reboot control

### AI Pi Lite firmware

Owns hardware I/O only:

- boot and provisioning
- Wi-Fi
- stable device identity
- microphone capture
- speaker playback
- display rendering
- buttons/touch
- LED state
- local telemetry
- local Hermes transport client
- OTA support later

## Donor adaptation strategy

### From Hermes-AIPI-lite

Reuse or adapt:

- WebSocket bridge concepts
- HERM binary audio framing
- device telemetry/control model
- device enumeration
- barge-in semantics

Remove or isolate:

- Linux systemd assumptions
- VPS-first deployment assumptions
- remote MCP as a hard dependency
- Linux filesystem conventions

### From Buddy / hermes-esp32-face / Xiaozhi

Reuse or adapt:

- ESP32-S3 project structure
- audio and display hardware patterns
- face/avatar rendering ideas
- device state transitions

Do not merge unrelated Buddy application behavior into the firmware core.

## Bot routing rule

Every inbound device event includes a stable `device_id`.

The local registry resolves:

```text
device_id -> assigned_bot_id -> Hermes Bot session
```

A device can be reassigned without firmware changes.

## Session rule

Device identity, Bot identity, and conversation/session identity are separate concepts.

This allows:

- one Bot to move between physical endpoints
- one endpoint to switch Bots
- background Bots with no physical endpoint
- Bot-to-Bot delegation independent of device routing

## Future extension boundary

Later, the Windows Hermes Desktop may connect outward to O-ai.cloud or a VPS-hosted MCP/tool fabric. That future link must sit below or beside Hermes tool access and must not change the endpoint contract defined here.
