# Financial Closing Advisor Agent

Financial Closing Cockpit AI Agent for Financial Controllers

## Business challenge

Financial controllers managing the period-end closing cycle spend significant time manually monitoring the status, priority, and sequencing of closing tasks across SAP Financial Closing Cockpit. They struggle to identify which tasks are blocked, determine root causes of failures, and decide what to action next — especially under tight deadlines. The agent automates this oversight: it retrieves current task statuses, evaluates the dependency chain, surfaces blocked and at-risk activities, recommends the next best actions in the correct sequence with clear reasoning, and supports configuration of closing calendar, ownership, escalation thresholds, and deadline proximity alerts.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Reduction in manual closing status review time | — | 50% | — | Financial Closing Task Monitoring | agent-derived |
| Average financial closing cycle duration | — | -2 days | — | Perform Accounting and Financial Close | agent-derived |
| Blocked task resolution time (root cause to action) | — | -60% | — | Dependency Chain Management | agent-derived |

## Key Milestones

1. **Closing status retrieved** — Agent successfully queries SAP Advanced Financial Closing (AFC) and returns the current status of all tasks for the active closing period.
2. **Dependency chain evaluated** — Agent maps task prerequisites and identifies the critical path; blocked and at-risk tasks are surfaced with root-cause context.
3. **Prioritised action list generated** — Agent recommends the next closing activities in correct sequence with clear reasoning per task.
4. **Blocker resolved** — Agent identifies root cause of a blocked task (missing data, upstream incomplete, system error) and suggests a corrective action that the controller can execute.
5. **Deadline alert triggered** — Agent detects tasks approaching their deadline threshold and escalates to the responsible owner per configured escalation rules.

## Business Architecture (RBA)

### End-to-End Process

Finance — Record to Report

### Process Hierarchy

```
Finance (E2E)
└── Record to Report (generic)
    └── Perform accounting and financial close (BPS-413)
        └── Perform financial closing
        └── Monitor closing task status and priorities
        └── Manage task dependencies and sequencing
        └── Identify and resolve blocked closing activities
        └── Escalate deadline-critical tasks
```

### Summary

The agent maps directly to BPS-413 "Perform accounting and financial close (generic)" within the Record to Report E2E, specifically the monitoring, sequencing, and corrective-action aspects of the financial close process.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Monitor closing task status and priorities | SAP Advanced Financial Closing (Local & Group Financial Closing) | `sap.afc:apiResource:SSPIV1:v1` | — | — | — | — | Yes | AFC Scheduling Service Provider API unavailable in this landscape; agent skill layer required |
| Task dependency chain evaluation | SAP Advanced Financial Closing | — | — | — | — | — | Yes | No direct dependency-chain API exposed; agent must derive from task metadata and sequence rules |
| Recommend next actions in sequence | SAP Advanced Financial Closing + SAP S/4HANA Finance | — | — | — | — | — | Yes | Reasoning and sequencing logic built into agent system prompt and skill layer |
| Identify root cause of blocked tasks | SAP Advanced Financial Closing, SAP Risk and Assurance Management | — | — | — | — | — | Yes | Root-cause analysis is an AI reasoning capability; no standard API covers this |
| Closing calendar and task ownership config | SAP Advanced Financial Closing | `sap.afc:apiResource:SCIMV2:v1` | — | — | — | — | Yes | SCIM API unavailable; ownership config handled via agent-managed configuration file |
| Escalation thresholds and deadline alerts | SAP Advanced Financial Closing, SAP Analytics Cloud | — | — | — | — | — | Yes | No standard alert API available; agent implements deadline proximity logic internally |

### Key findings

- SAP Advanced Financial Closing (AFC) is the primary standard product covering BPS-413; it provides mandatory capabilities for Local and Group Financial Closing.
- All AFC-specific APIs discovered (`sap.afc:apiResource:SSPIV1:v1`, `sap.afc:apiResource:TaskProviderV2:v1`, `sap.afc:apiResource:SCIMV2:v1`) are marked **unavailable** in this landscape — the agent must use AFC's available interfaces or a custom skill layer.
- The Finance Freeze Period API (`sap.s4:apiResource:RACONTRSETFREEZEPERDSIN:v1`) is available in S/4HANA and can be leveraged for period-status checks.
- SAP S/4HANA Cloud (Public and Private Edition) provides mandatory coverage for financial analytics, audit preparation, and general ledger — these can be surfaced via agent tool calls.
- Dependency-chain reasoning and root-cause analysis are AI reasoning capabilities with no direct standard API equivalent — they are core differentiators of this agent solution.
- Escalation and deadline proximity alerting must be implemented within the agent logic, as no dedicated alert API is available in the current landscape.

## Recommendations

### Financial Closing Advisor AI Agent

#### Executive Summary

Pro-code Python A2A agent integrating with SAP AFC and S/4HANA Finance to guide financial controllers through each closing cycle.

#### Recommended Solution

A Python-based AI agent (A2A protocol) deployed on SAP BTP, integrating with SAP Advanced Financial Closing and SAP S/4HANA Finance. The agent retrieves closing task statuses, evaluates the dependency chain, identifies blockers with root-cause reasoning, recommends prioritised next actions, and proactively alerts on deadline proximity. Configuration for closing calendar, task ownership, escalation thresholds, and deadline alerts is managed via agent-level configuration. MCP tool calls connect to available S/4HANA Finance APIs; AFC integration uses a custom skill layer where AFC APIs are unavailable.

#### Recommended solution category

AI Agent

#### Intent fit
88%
