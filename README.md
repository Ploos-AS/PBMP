# PBMP — Ploos Bot Management Protocol

PBMP is an implementation-neutral management protocol for IRC bots and related agents. LuCa and Engo are initial implementations; neither is privileged by the protocol.

M0 defines PBMP/1 discovery, capabilities, status and events as JSON messages. The transport is deliberately separable from the message model so local sockets, pipes or authenticated network transports can be qualified independently.

See [spec/PBMP-1.md](spec/PBMP-1.md).

License: MIT.
