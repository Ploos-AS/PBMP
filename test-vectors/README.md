# PBMP/1 conformance test vectors

These vectors provide implementation-neutral fixtures for PBMP/1 parsers and transports.

## Layout

- `valid/` contains messages that a conforming PBMP/1 envelope parser MUST accept.
- `invalid/` contains messages that a conforming parser MUST reject.
- `methods/` contains canonical request/response pairs for the required PBMP/1 M0 methods.
- `methods-invalid/` contains semantically invalid required-method responses that the conformance validator MUST reject.

Method-specific semantic vectors will be added separately so envelope conformance and method conformance remain independently testable.

The vectors intentionally do not require BotWeb, BotAI, LuCa, Engo, or any other implementation.

## M0 required-method coverage

The current vectors cover `pbmp.info`, `capabilities.list`, `bot.info`, and `networks.list`. Implementations claiming PBMP/1 M0 conformance MUST implement all four required methods and preserve request IDs in responses.

The validator checks both the common PBMP envelope and the minimum result structure of each required M0 method. Negative semantic vectors prevent an implementation from passing merely by returning syntactically valid JSON.
