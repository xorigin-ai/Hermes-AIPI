# Device-to-Bot Model

## Principle

Bots are portable persistent identities. AI Pi Lite units are addressable physical endpoints.

## Device record

```json
{
  "device_id": "aipi-01",
  "name": "Office One",
  "transport": "ws",
  "host": "auto",
  "default_bot_id": "research",
  "capabilities": {
    "microphone": true,
    "speaker": true,
    "display": true,
    "led": true,
    "buttons": true,
    "battery": true
  }
}
```

## Assignment rules

- `device_id` is stable across reboot.
- `default_bot_id` is stored on the Windows Hermes host, not hardcoded in firmware.
- A device may be reassigned at runtime.
- A Bot may exist without a device.
- Multiple devices may eventually target the same Bot, but the initial POC should default to one-to-one mapping for clarity.

## Initial five-device demo mapping

```text
AI Pi 01 -> General Bot
AI Pi 02 -> Research Bot
AI Pi 03 -> Coding Bot
AI Pi 04 -> Operations Bot
AI Pi 05 -> Specialist Bot
```

The exact Bot names are configuration, not protocol.

## Routing lifecycle

```text
1. Device connects.
2. Hermes-AIPI validates device_id.
3. Registry loads assigned_bot_id.
4. Device opens an interaction/session.
5. Input is routed to the assigned Hermes Bot.
6. Bot may call apps/tools or delegate to another Bot.
7. Result returns to the originating device session.
8. Display/LED state follows the session lifecycle.
```

## State model

```text
OFFLINE -> IDLE -> LISTENING -> THINKING -> SPEAKING -> IDLE
                          \-> ERROR -> IDLE
```

Barge-in during `SPEAKING` immediately stops output and moves the device to `LISTENING`.

## Persistence test

After rebooting both Windows and all five endpoints, the same `device_id -> default_bot_id` mappings must be restored without reflashing or manually recreating Bots.
