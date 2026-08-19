# POC Contract

## Objective

Prove the newly introduced Hermes Desktop Bot Mode as a persistent multi-Bot operating model with five physical AI Pi Lite endpoints on a single local Windows 11 network.

## Architectural invariant

The Bot is the agent. The AI Pi Lite is an endpoint.

Each Bot owns or references its own:

- name and identity
- role
- model
- memory
- skills
- profile picture/avatar
- conversation/session context

AI Pi Lite devices provide physical I/O and device state only.

## Local-only boundary

The POC must operate without:

- O-ai.cloud
- a VPS
- remote MCP servers
- a remote orchestration plane

Future remote connectivity is allowed only after this local contract is proven.

## Required demonstrations

### Bot persistence

Create at least five Bots. Restart Hermes Desktop and confirm the same Bots remain available with their profiles intact.

### Device persistence

Pair five devices. Restart the Windows host and each device. Confirm device identity and assignment survive.

### Device-to-Bot mapping

Each endpoint has a default Bot. Mapping can be changed without reflashing firmware.

### Voice round trip

Endpoint microphone -> local transport -> Hermes -> selected Bot -> response audio -> originating endpoint.

### Physical state

Hermes can drive listening, thinking, speaking, idle, and error states on the endpoint display/LED.

### Existing app invocation

A Bot can call at least one already-built Hermes-compatible application or integration.

### Bot-to-Bot delegation

One Bot requests work from a second Bot and then uses the returned result in its own response or action.

### Offline/local test

After local models and dependencies are installed, disconnect WAN access and run the core demonstration.

## Non-goals

This POC is not a production security review, cloud deployment, fleet-management platform, commercial provisioning workflow, or remote MCP architecture.

## Success statement

The POC succeeds when one clean Windows 11 Hermes Desktop machine can persistently operate a team of named specialist Bots through five local AI Pi Lite endpoints, with no external control plane required.
