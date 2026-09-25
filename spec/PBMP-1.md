# PBMP/1 — M0 specification

Status: **M0 draft**

## Principles

PBMP is versioned, capability-driven and bot-implementation-neutral. A client MUST discover capabilities instead of assuming optional methods. Bot operation MUST NOT depend on a PBMP client being present.

## Envelope

Every UTF-8 JSON message contains `pbmp: 1` and `type`. Requests additionally contain a client-generated `id`. Responses echo that `id`.

Request:

    {"pbmp":1,"type":"request","id":"42","method":"bot.info","params":{}}

Success:

    {"pbmp":1,"type":"response","id":"42","ok":true,"result":{}}

Error:

    {"pbmp":1,"type":"response","id":"42","ok":false,"error":{"code":"not_supported","message":"method not supported"}}

Event:

    {"pbmp":1,"type":"event","event":"bot.connected","data":{"network":"libera"}}

## M0 required methods

* `pbmp.info` — protocol version and implementation metadata.
* `capabilities.list` — supported optional capabilities and methods.
* `bot.info` — bot identity, implementation name/version and lifecycle state.
* `networks.list` — configured networks and connection state.

## Initial optional capabilities

* `channels.list`
* `modules.list`
* `scripts.list`
* `logs.stream`
* `metrics.read`
* `config.schema`
* `config.read`
* `config.write`
* `commands.execute`

Capabilities are additive. Unknown capabilities MUST be ignored by clients.

## Security

PBMP/1 does not define anonymous remote administration. A network-accessible transport MUST authenticate peers and provide confidentiality and integrity. Implementations SHOULD default to a local-only transport. Authorization SHOULD be capability/method scoped. Secrets MUST NOT be returned by configuration APIs unless a future specification explicitly defines a protected secret mechanism.

## Compatibility

New optional fields may be added within PBMP/1. Receivers MUST ignore unknown fields. Breaking envelope or required-method changes require a new PBMP major version.
