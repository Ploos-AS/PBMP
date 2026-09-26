# PBMP — Ploos Bot Management Protocol

PBMP is an implementation-neutral management protocol for IRC bots and related agents. LuCa and Engo are initial implementations; neither is privileged by the protocol.

M0 defines PBMP/1 discovery, capabilities, status and events as JSON messages. The transport is deliberately separable from the message model so local sockets, pipes or authenticated network transports can be qualified independently.

## Standalone-first rule

PBMP is an optional management integration. A PBMP-compatible IRC bot MUST NOT require PBMP, BotWeb, BotAI, or another external Ploos service for normal IRC operation. Implementations MUST treat PBMP as an adapter/control interface around an independently functional bot core. Loss or disablement of PBMP MUST NOT stop the bot's IRC service.

See [spec/PBMP-1.md](spec/PBMP-1.md).

License: MIT.
