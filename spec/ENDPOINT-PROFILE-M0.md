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

An endpoint MAY include `uptime_seconds` in the `endpoint` object. When present, it MUST be a non-negative integer representing elapsed whole seconds since the current endpoint process/service instance started. It is runtime telemetry, not wall-clock time, and MUST reset when that instance restarts. Clients MUST NOT assume that its absence means the endpoint has just started.

Initial generic kinds include `bot`, `agent`, `service`, and `gateway`. The value `bouncer` is defined for IRC bouncer/BNC services such as AmBNC.

## Optional IRC management

An IRC-aware endpoint MAY advertise `networks.list`, `channels.list`, and other IRC-related PBMP capabilities. Their absence does not fail Endpoint Profile M0 qualification.

## Network observability reference

AmBNC is the initial reference implementation for the optional PBMP/1 `networks.list` runtime observability fields `retry_seconds`, `reconnect_attempts`, `connected_seconds`, and `paused` defined by the base PBMP/1 specification.

AmBNC has been qualified with Endpoint Profile M0 against PBMP conformance-suite revision `b8c9ff18fca516a118a7a45001860e5de9c95da3`, including the network observability semantic vectors. This reference status does not make `networks.list` or any observability field mandatory for Endpoint Profile M0, and other implementations MAY expose the same standard fields with implementation-appropriate internal mechanisms.

The reference contract is deliberately read-only and excludes network credentials and authentication material.

## Standalone operation

PBMP remains optional infrastructure. Qualification against this profile MUST NOT require BotWeb, BotAI, or another Ploos service, and loss or disablement of PBMP MUST NOT stop the endpoint's primary service.

## Relationship to the Bot Profile

The existing PBMP/1 M0 bot contract remains unchanged. A bot may implement both `bot.info` and `endpoint.info`. Endpoint Profile M0 is an additional conformance profile, not a replacement for the bot profile.
