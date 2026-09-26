# PBMP/1 conformance test vectors

These vectors provide implementation-neutral fixtures for PBMP/1 parsers and transports.

## Layout

- `valid/` contains messages that a conforming PBMP/1 envelope parser MUST accept.
- `invalid/` contains messages that a conforming parser MUST reject.

Method-specific semantic vectors will be added separately so envelope conformance and method conformance remain independently testable.

The vectors intentionally do not require BotWeb, BotAI, LuCa, Engo, or any other implementation.
