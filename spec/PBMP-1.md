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
* `channels.join`
* `channels.part`
* `modules.list`
* `modules.reload`
* `modules.enable`
* `modules.disable`
* `scripts.list`
* `logs.stream`
* `metrics.read`
* `config.schema`
* `config.read`
* `config.write`
* `commands.execute`

Capabilities are additive. Unknown capabilities MUST be ignored by clients.

## `modules.list`

A bot advertising `modules.list` MUST accept an empty params object and return a `modules` array. Each module MUST contain a stable `id` for the current bot configuration, a `runtime` identifier, and an extensible `state` string. Initial states are `active`, `disabled`, and `error`. An optional `capabilities` array describes permissions/features granted to that module.

Example:

    {"modules":[{"id":"hello.tengo","runtime":"tengo","state":"active","capabilities":["http"]}]}

The method is read-only. `runtime` identifies the execution environment (for example `lua`, `tengo`, or `arexx`) and MUST NOT be used by clients to infer management capabilities; those remain PBMP capabilities.

## `modules.reload`, `modules.enable`, and `modules.disable`

These are independent write capabilities. Each accepts `{"id":"module-id"}`. Advertising `modules.list` MUST NOT imply lifecycle control. A successful response means the requested lifecycle transaction completed and returns `{"id":"module-id","state":"active"}` (or `disabled`). Reload implementations SHOULD preserve the previously active module when validation/loading of the replacement fails. Enable/disable SHOULD be transactional where the runtime supports rollback. Unsupported lifecycle operations MUST not be advertised.

## `channels.list`

A bot advertising `channels.list` MUST accept an empty params object and return:

    {"channels":[{"network":"libera","name":"#example","state":"joined"}]}

Each channel object MUST contain `network`, `name`, and `state`. `state` is an extensible string; initial values are `joined`, `configured`, and `disconnected`. Clients MUST tolerate unknown states. The method is read-only and MUST NOT join or part channels as a side effect.

## `channels.join` and `channels.part`

These are independent write capabilities. Advertising `channels.list` MUST NOT imply permission or support for either write operation.

`channels.join` accepts `{"network":"libera","name":"#example"}`. `channels.part` accepts the same fields plus an optional `reason` string. A successful request means the command was accepted for transmission; it does not claim that the IRC server has completed the operation. Implementations MUST validate that the requested network identifies the managed connection and that `name` is a syntactically safe IRC channel target. Invalid input returns `invalid_params` and MUST NOT be sent to IRC.

Successful result:

    {"network":"libera","name":"#example","state":"joining"}

For PART, the immediate state is implementation-dependent (normally `parting` or `configured`) and clients MUST continue to use `channels.list` for authoritative observed state.

## Security

PBMP/1 does not define anonymous remote administration. A network-accessible transport MUST authenticate peers and provide confidentiality and integrity. Implementations SHOULD default to a local-only transport. Authorization SHOULD be capability/method scoped. Secrets MUST NOT be returned by configuration APIs unless a future specification explicitly defines a protected secret mechanism.

## Compatibility

New optional fields may be added within PBMP/1. Receivers MUST ignore unknown fields. Breaking envelope or required-method changes require a new PBMP major version.
