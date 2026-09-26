# PBMP integration architecture

PBMP is the management plane for independently functional bots, agents, and related services. It is not an application data plane and it is not owned by BotWeb or BotAI.

## BotWeb

BotWeb is an optional PBMP client. It discovers endpoint capabilities and builds management UI from the methods an endpoint advertises. BotWeb MUST NOT be required for normal operation of a PBMP-managed bot or service.

BotWeb SHOULD use PBMP for status, network/channel management, modules, metrics, logs, and safe configuration where those capabilities are advertised. It SHOULD NOT require implementation-specific management APIs when an equivalent PBMP capability exists.

## BotAI

BotAI integration has two distinct paths:

1. Runtime AI traffic between a bot and BotAI uses a BotAI application API/protocol, not PBMP.
2. Management and observability MAY use PBMP.

Prompts, generated replies, model streaming, and other high-volume AI runtime traffic MUST NOT be tunneled through PBMP/1 M0.

Future optional PBMP capabilities MAY expose AI management information such as AI health, roles, providers, models, sessions, or metrics. Such capabilities remain optional and capability-discovered.

BotAI MAY itself expose a PBMP management endpoint while remaining operational independently of PBMP and BotWeb.

## Failure isolation

Loss, disablement, or absence of PBMP MUST NOT stop the primary bot/service function. Loss of BotWeb MUST NOT stop a managed endpoint. Loss of BotAI MUST NOT stop ordinary IRC operation unless an explicitly AI-only feature is invoked.

## Dependency direction

The intended dependency direction is:

```
BotWeb -> PBMP -> managed endpoint
IRC bot -> BotAI application API (optional)
BotWeb -> PBMP -> BotAI management endpoint (optional)
```

PBMP therefore standardizes management interoperability without becoming a mandatory runtime dependency or an AI message transport.
