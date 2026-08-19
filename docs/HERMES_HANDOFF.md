# Hermes Handoff

This repository is the implementation contract for the local Windows 11 Hermes Desktop Bot Mode proof of concept.

## Mission

Finish and validate a local system in which one fresh Windows 11 Hermes Desktop machine manages five AI Pi Lite physical endpoints. Hermes Desktop Bot Mode is the central proof point. Each endpoint is assigned to a persistent Hermes Bot profile. Bots own cognition; endpoints own physical I/O.

## Hard scope boundary

Do not add:

- VPS deployment
- O-ai.cloud
- remote/shared MCP control plane
- cloud orchestration

Those are future extensions only after the local POC passes.

## Source authority

1. Current Nous Research Hermes Desktop implementation/documentation for Bot Mode/profile behavior.
2. This repository for the local device contract.
3. `xorigin-ai/Hermes-AIPI-lite` for HERM framing, hardware bridge, telemetry/control patterns.
4. `xorigin-ai/Buddy/hermes-esp32-face/firmware/xiaozhi` for ESP32-S3 firmware patterns.
5. `xorigin-ai/Buddy/buddy_gibbertalk_ai_studio_handoff` for optional voice/avatar/protocol donor material.

Preserve source licenses and provenance. Do not copy Linux/VPS assumptions into this Windows-local architecture.

## Existing runtime scaffold

The repo already contains:

- persistent five-device registry
- 16-byte HERM audio framing
- local WebSocket bridge
- stable device handshake using firmware-provided `device_id`
- `device_id -> Hermes Bot profile` routing field
- runtime reassignment persistence
- audio routing callbacks
- display/state JSON channel
- barge-in stream invalidation
- Windows bootstrap script
- protocol and persistence unit tests

## Critical implementation rule

Do not create a second agent runtime or fake Bot database. Treat Hermes Bot profiles as authoritative identities. The local bridge stores only the mapping from physical `device_id` to Hermes profile/Bot identifier and session routing state.

## Required execution sequence

1. Install/verify the current Hermes Desktop build with Bot Mode on Windows 11.
2. Determine the current local programmatic profile/session interface from the installed/current Hermes source. Do not guess commands or undocumented APIs.
3. Wire `LocalBridge.on_audio` and device events into the assigned Hermes Bot profile.
4. Wire Hermes response audio/state callbacks back to the originating AI Pi Lite.
5. Prove one device end-to-end before cloning the endpoint configuration to five devices.
6. Adapt firmware from the cited ESP32/Xiaozhi donor so it sends `device.hello`, streams HERM PCM frames, receives speaker frames, renders state/avatar updates, sends buttons/telemetry, and reconnects automatically.
7. Run the acceptance checklist in `docs/POC_CONTRACT.md`.
8. Reboot Windows and all devices and prove Bot profiles and device assignments persist.
9. Disconnect WAN after any required local assets are installed and rerun the core demo.

## Five initial Bot mappings

- `aipi-01` -> `general`
- `aipi-02` -> `research`
- `aipi-03` -> `coding`
- `aipi-04` -> `operations`
- `aipi-05` -> `specialist`

These identifiers may be changed to the actual Hermes profile IDs/names created on the fresh box.

## Definition of done

Do not declare the POC complete merely because the bridge starts or devices connect. It is complete only when a physical AI Pi Lite voice turn is routed into its assigned persistent Hermes Bot, response audio returns to the same endpoint, runtime reassignment works, Bot-to-Bot delegation is demonstrated, an existing Hermes-compatible app is invoked, and persistence survives reboot.
