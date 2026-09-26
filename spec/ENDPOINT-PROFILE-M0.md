# PBMP/1 Endpoint Profile M0

Status: **M0 draft**

The Endpoint Profile defines the minimum PBMP management contract for independently functional services that are not necessarily IRC bots. AmBNC is the initial reference consumer for this profile.

## Required methods

An Endpoint Profile M0 implementation MUST implement:

- `pbmp.info`
- `capabilities.list`
- `endpoint.info`

It MUST NOT be required to implement `bot.info` or `networks.list` merely to qualify for this profile.

## endpoint.info

Request parameters are empty.

A successful result has this form:

```json
{
  "endpoint": {
    "id": "ambnc",
    "kind": "bouncer",
    "implementation": {
      "name": "AmBNC",
      "version": "0.1.0"
    },
    "state": "running"
  }
}
```

`id`, `kind`, `implementation.name`, `implementation.version`, and `state` MUST be non-empty strings. Endpoint IDs MUST be stable within the management endpoint. Clients MUST tolerate unknown `kind` and `state` values.

Initial generic kinds include `bot`, `agent`, `service`, and `gateway`. The value `bouncer` is defined for IRC bouncer/BNC services such as AmBNC.

## Optional IRC management

An IRC-aware endpoint MAY advertise `networks.list`, `channels.list`, and other IRC-related PBMP capabilities. Their absence does not fail Endpoint Profile M0 qualification.

## Standalone operation

PBMP remains optional infrastructure. Qualification against this profile MUST NOT require BotWeb, BotAI, or another Ploos service, and loss or disablement of PBMP MUST NOT stop the endpoint's primary service.

## Relationship to the Bot Profile

The existing PBMP/1 M0 bot contract remains unchanged. A bot may implement both `bot.info` and `endpoint.info`. Endpoint Profile M0 is an additional conformance profile, not a replacement for the bot profile.
