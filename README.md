# PBMP — Ploos Bot Management Protocol

PBMP is an implementation-neutral management protocol for IRC bots and related agents. LuCa and Engo are initial implementations; neither is privileged by the protocol.

M0 defines PBMP/1 discovery, capabilities, status and events as JSON messages. The transport is deliberately separable from the message model so local sockets, pipes or authenticated network transports can be qualified independently.

## Standalone-first rule

PBMP is an optional management integration. A PBMP-compatible IRC bot MUST NOT require PBMP, BotWeb, BotAI, or another external Ploos service for normal IRC operation. Implementations MUST treat PBMP as an adapter/control interface around an independently functional bot core. Loss or disablement of PBMP MUST NOT stop the bot's IRC service.

See [spec/PBMP-1.md](spec/PBMP-1.md). Integration boundaries for BotWeb, BotAI, and other consumers are defined in [spec/INTEGRATIONS.md](spec/INTEGRATIONS.md).

## Conformance

PBMP/1 M0 includes implementation-neutral conformance vectors and a dependency-free validator. Implementations can publish a machine-readable qualification report tied to the exact implementation version and PBMP suite revision used for testing.

See [spec/CONFORMANCE.md](spec/CONFORMANCE.md) and [schema/conformance-report.schema.json](schema/conformance-report.schema.json).

License: MIT.

## Conformance profiles

PBMP/1 currently defines the original M0 bot contract and the additive [Endpoint Profile M0](spec/ENDPOINT-PROFILE-M0.md). The endpoint profile is intended for managed services that are not necessarily bots; AmBNC is its initial reference consumer.
