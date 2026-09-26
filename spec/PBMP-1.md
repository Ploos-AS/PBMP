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

## Required method contracts

### `pbmp.info`

Accepts an empty params object and returns `{"version":1,"implementation":{"name":"...","version":"..."}}`. `version` MUST be the PBMP major version implemented by the endpoint. The implementation object MUST contain non-empty `name` and `version` strings. Additional implementation metadata MAY be returned and MUST be ignored when unknown.

### `capabilities.list`

Accepts an empty params object and returns `{"capabilities":[...]}`. Each entry MUST be a non-empty string naming an optional PBMP capability/method supported by the endpoint. The array MUST NOT be interpreted as granting authorization by itself; transport or endpoint policy MAY further restrict an advertised write method. Clients MUST ignore unknown capability names.

### `bot.info`

Accepts an empty params object and returns `{"bot":{"id":"...","implementation":{"name":"...","version":"..."},"state":"..."}}`. `id` MUST be a stable non-empty identifier for the bot within the management endpoint. Initial lifecycle states are `starting`, `running`, `stopping`, `stopped`, and `error`; clients MUST tolerate unknown states.

### `networks.list`

Accepts an empty params object and returns `{"networks":[...]}`. Each network MUST contain a stable non-empty `id` and an extensible `state` string. Initial states are `configured`, `connecting`, `connected`, `disconnecting`, `disconnected`, and `error`. A network MAY include a human-readable `name`. Clients MUST use `id`, not `name`, as the management identifier and MUST tolerate unknown states.

## General managed endpoint identity

PBMP/1 M0 remains bot-oriented and keeps `bot.info` as a required method for the M0 bot profile. Non-bot services MUST NOT fabricate a bot identity merely to reuse PBMP.

The optional `endpoint.info` capability provides general identity for bots, agents, services, gateways, and other managed endpoints. It accepts an empty params object and returns:

```json
{"endpoint":{"id":"stable-id","kind":"service","implementation":{"name":"example","version":"1.0.0"},"state":"running"}}
```

`id` MUST be a stable non-empty management identifier. `kind` MUST be a non-empty string. Initial kinds are `bot`, `agent`, `service`, and `gateway`; clients MUST tolerate unknown kinds. `implementation.name`, `implementation.version`, and `state` MUST be non-empty strings.

A bot MAY advertise `endpoint.info` in addition to required `bot.info`. When both describe the same managed process, their stable identity and implementation metadata SHOULD be consistent.

Support for `endpoint.info` does not by itself define a non-bot conformance profile. Such a profile requires a future specification; PBMP/1 M0 conformance continues to require the four M0 bot methods.

## Initial optional capabilities

* `endpoint.info`
* `channels.list`
* `channels.join`
* `channels.part`
* `modules.list`
* `modules.reload`
* `modules.enable`
* `modules.disable`
* `scripts.list`
* `logs.read`
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

Each channel object MUST contain `network`, `name`, and `state`. `state` is an extensible string; initial values are `joined`, `configured`, `joining`, `parting`, and `disconnected`. Clients MUST tolerate unknown states. The method is read-only and MUST NOT join or part channels as a side effect.

## `channels.join` and `channels.part`

These are independent write capabilities. Advertising `channels.list` MUST NOT imply permission or support for either write operation.

`channels.join` accepts `{"network":"libera","name":"#example"}`. `channels.part` accepts the same fields plus an optional `reason` string. A successful request means the command was accepted for transmission; it does not claim that the IRC server has completed the operation. Implementations MUST validate that the requested network identifies the managed connection and that `name` is a syntactically safe IRC channel target. Invalid input returns `invalid_params` and MUST NOT be sent to IRC.

Successful result:

    {"network":"libera","name":"#example","state":"joining"}

For PART, the immediate state is implementation-dependent (normally `parting` or `configured`). Runtime-requested channels SHOULD remain discoverable through `channels.list` while their join/part lifecycle is relevant; clients MUST NOT assume the startup configuration is the complete registry; clients MUST continue to use `channels.list` for authoritative observed state.

## `metrics.read`

Read-only snapshot metrics. An implementation SHOULD return counters/gauges it can measure reliably under a `metrics` object. Common names are `irc.rx_lines`, `irc.tx_lines`, `irc.reconnects`, and `session.uptime_seconds`. Values MUST be JSON numbers. Clients MUST tolerate unknown or missing metric names.

## `logs.read`

Read-only bounded recent-log retrieval. The result is `{"entries":[...]}`; each entry contains `level` and `message`, with optional `time` and `source`. Implementations MUST bound retained entries and response size. Secrets and credentials MUST NOT be logged or returned. `logs.read` is snapshot/polling and is distinct from the reserved `logs.stream` event/subscription capability.

`logs.stream` remains reserved until PBMP defines subscription lifetime and multi-message transport framing.

## `config.schema` and `config.read`

These methods expose a deliberately safe management view, not the process environment or raw configuration file. `config.schema` returns `{"fields":[...]}`; each field has `name`, `type`, and `reload` where reload is `live`, `reconnect`, or `restart`. `config.read` returns `{"config":{...}}` containing only fields present in that schema.

Secret values, credential identifiers, passwords, authentication tokens, private keys, and implementation-local management endpoints MUST NOT be returned. Implementations SHOULD omit sensitive policy fields when disclosure is unnecessary for ordinary bot operation. Advertising either read capability does not imply `config.write`.

## Local stream transport profile

The PBMP/1 local stream profile uses UTF-8 JSON Lines. Each connection carries exactly one request line followed by exactly one response line. A line MUST end with LF; CRLF MAY be accepted. Receivers MUST reject an unterminated request, trailing non-whitespace data, or multiple request objects on one connection.

Implementations of this profile MUST accept request lines up to 4096 bytes including the line terminator and MUST bound larger input. Clients MUST accept response lines up to 16384 bytes including the line terminator; servers MUST NOT emit a larger response on this profile. Implementations MAY use smaller internal result limits only when every advertised method can still produce a conforming response. These limits are transport bounds, not permission to expose unbounded logs or configuration data.

## Security

PBMP/1 does not define anonymous remote administration. A network-accessible transport MUST authenticate peers and provide confidentiality and integrity. Implementations SHOULD default to a local-only transport. Authorization SHOULD be capability/method scoped. Secrets MUST NOT be returned by configuration APIs unless a future specification explicitly defines a protected secret mechanism.

## Compatibility

New optional fields may be added within PBMP/1. Receivers MUST ignore unknown fields. Breaking envelope or required-method changes require a new PBMP major version.
