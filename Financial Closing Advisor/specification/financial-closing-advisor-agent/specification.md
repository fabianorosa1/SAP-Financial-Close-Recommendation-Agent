# Specification: financial-closing-advisor-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` for full context before starting.
- [x] Bootstrap agent code in `assets/financial-closing-advisor-agent/` using the `sap-agent-bootstrap` skill instructions. Invoke from inside `assets/financial-closing-advisor-agent/` and use copy commands — do NOT create files manually.
- [x] Install dependencies and validate the agent starts and responds at `/.well-known/agent.json`.

---

## Runtime Skills

The agent requires runtime skills for the following domain areas (decision: complex multi-step workflows with conditional logic and domain-specific rules):

- [x] Create `assets/financial-closing-advisor-agent/app/skills/closing-task-monitor/SKILL.md` with:
  - YAML frontmatter: `name: closing-task-monitor`, `description: Retrieves and presents the status of all financial closing tasks for the active period, including status, owner, priority, and deadline.`
  - Body: Step-by-step instructions to retrieve all tasks, classify each as completed/in-progress/blocked/pending, and return a structured summary with task ID, description, status, owner, priority, and deadline.
  - Companion file: `assets/financial-closing-advisor-agent/app/skills/closing-task-monitor/references/task-status-definitions.md` — defines the meaning of each status category (completed, in-progress, blocked, pending) and how to identify them from task metadata.

- [x] Create `assets/financial-closing-advisor-agent/app/skills/dependency-chain-evaluator/SKILL.md` with:
  - YAML frontmatter: `name: dependency-chain-evaluator`, `description: Evaluates the task dependency chain for the current closing plan, identifies the critical path, and surfaces blocked and at-risk tasks with their upstream dependency context.`
  - Body: Instructions to map task prerequisites from the task list, identify which pending/blocked tasks are dependencies for other tasks, determine the critical path (longest chain to close completion), and annotate each blocked task with its upstream dependency task ID and reason for blocking.

- [x] Create `assets/financial-closing-advisor-agent/app/skills/next-action-recommender/SKILL.md` with:
  - YAML frontmatter: `name: next-action-recommender`, `description: Recommends the next financial closing activities in the correct execution sequence with reasoning, based on current task statuses and the dependency chain.`
  - Body: Instructions to filter for actionable tasks (pending tasks whose upstream dependencies are complete), rank them by priority and deadline proximity, and return an ordered action list with task ID, recommended action, and justification per task.
  - Companion reference: `assets/financial-closing-advisor-agent/app/skills/next-action-recommender/references/prioritisation-rules.md` — defines the prioritisation logic (deadline proximity > task priority level > dependency chain depth).

- [x] Create `assets/financial-closing-advisor-agent/app/skills/blocker-root-cause-analyzer/SKILL.md` with:
  - YAML frontmatter: `name: blocker-root-cause-analyzer`, `description: Identifies the root cause of a blocked closing task (missing data, incomplete upstream task, system error, or configuration issue) and suggests a corrective action the financial controller can execute.`
  - Body: Decision tree for root-cause classification:
    - If upstream task is incomplete → "Upstream task [ID] not yet completed; action the upstream task first."
    - If task has a system error message → relay the error message and suggest re-running or contacting system administrator.
    - If required data fields are missing → list the specific missing fields and their data owners.
    - If configuration is absent → identify the missing configuration parameter and direct to the closing configuration.
  - Companion file: `assets/financial-closing-advisor-agent/app/skills/blocker-root-cause-analyzer/references/error-patterns.md` — common AFC error patterns and their corrective actions.

- [x] Create `assets/financial-closing-advisor-agent/app/skills/deadline-alert-manager/SKILL.md` with:
  - YAML frontmatter: `name: deadline-alert-manager`, `description: Detects tasks approaching their configured deadline proximity threshold and generates escalation alerts identifying the at-risk task, owner, remaining time, and recommended escalation action.`
  - Body: Instructions to compare each task's remaining time against the configured alert threshold from the closing configuration, identify tasks below threshold, generate a structured alert per task including task ID, owner, remaining hours, and recommended escalation step.
  - Companion file: `assets/financial-closing-advisor-agent/app/skills/deadline-alert-manager/references/escalation-matrix.md` — defines escalation levels (warning / critical / breach) and the corresponding escalation actions per level.

---

## Project-Specific Tasks

### System Prompt

- [x] Open `assets/financial-closing-advisor-agent/app/agent.py` and update the `get_system_prompt()` function with the following:
  - Role: "You are the Financial Closing Advisor, an AI agent that supports financial controllers during the period-end financial closing cycle."
  - Core capabilities: monitoring closing task status, evaluating dependency chains, recommending next actions in sequence, identifying root causes of blockers, and triggering deadline proximity alerts.
  - Instruction to never fabricate or invent financial data — always use tools to retrieve live data from the closing task store and configuration.
  - Instruction to relay tool errors verbatim without embellishment.
  - Instruction that all recommendations are advisory only; execution of corrective actions requires explicit controller confirmation.
  - Instruction to load the appropriate runtime skill before executing any multi-step task (task monitoring, dependency evaluation, action recommendation, root-cause analysis, deadline alerting).
  - Page size instruction: when calling tools that support pagination, set the page size parameter to a maximum of 100.

### Closing Task Data Store (Mock AFC Integration)

Since all SAP Advanced Financial Closing APIs are unavailable in this landscape, the agent uses a local mock data store for closing tasks that simulates AFC task data:

- [x] Create `assets/financial-closing-advisor-agent/app/closing_task_store.py` — a Python module that returns a static list of mock closing tasks for the active period. Each task must include: `task_id`, `description`, `status` (completed/in-progress/blocked/pending), `owner`, `priority` (high/medium/low), `deadline` (ISO datetime string), `dependencies` (list of task_ids this task depends on), `error_message` (optional, for blocked tasks), `missing_fields` (optional list of required data fields not yet populated).
  - Include at least 12 mock tasks representing a realistic month-end closing cycle: e.g. "Accounts Payable Reconciliation", "Accounts Receivable Clearing", "Fixed Asset Depreciation Run", "Inventory Valuation", "Intercompany Eliminations", "Foreign Currency Revaluation", "Accruals Posting", "Cost Centre Allocation", "Profit Centre Settlement", "Trial Balance Extraction", "Management Report Generation", "Period Lock".
  - Include at least 2 blocked tasks with error messages, 1 blocked task with missing fields, and 2 tasks with deadlines within the configured alert threshold.
  - Structure the dependency chain so that multiple tasks depend on earlier tasks (e.g. Trial Balance depends on all sub-ledger reconciliations completing).

- [x] Create `assets/financial-closing-advisor-agent/app/tools/get_closing_tasks.py` — a LangChain `StructuredTool` that calls `closing_task_store.py` and returns all closing tasks for the active period. Input: `period` (optional string, defaults to current period). Output: list of task dictionaries.

- [x] Create `assets/financial-closing-advisor-agent/app/tools/get_task_dependencies.py` — a LangChain `StructuredTool` that returns the dependency map for the current closing plan (which tasks depend on which). Derives the map from `closing_task_store.py`. Input: none required. Output: a dictionary mapping each task_id to its list of dependency task_ids.

- [x] Create `assets/financial-closing-advisor-agent/app/tools/get_period_status.py` — a LangChain `StructuredTool` that returns the open/closed status of the current financial period (mock implementation; returns a static dict with `period`, `status` [open/closed], `closing_deadline`).

### Closing Configuration Store

- [x] Create `assets/financial-closing-advisor-agent/app/closing_config_store.py` — a Python module that stores and retrieves closing configuration as a dictionary. Initial default configuration must include:
  - `closing_calendar`: list of entities with `entity_id`, `period`, `closing_date`
  - `task_ownership`: dict mapping `task_id` to `owner_email` and `owner_name`
  - `escalation_thresholds`: dict with severity levels `warning_hours` (default: 8), `critical_hours` (default: 4), `breach_hours` (default: 0)
  - `deadline_proximity_alert_hours`: default 6

- [x] Create `assets/financial-closing-advisor-agent/app/tools/get_closing_config.py` — a LangChain `StructuredTool` that reads the full current configuration from `closing_config_store.py`. Input: optional `section` (string) to return only a specific config section. Output: full config dict or specified section.

- [x] Create `assets/financial-closing-advisor-agent/app/tools/update_closing_config.py` — a LangChain `StructuredTool` that updates a specific configuration parameter in `closing_config_store.py`. Input: `section` (string), `key` (string), `value` (any). Output: confirmation message with updated value. Note: this tool performs writes — it must always confirm with the caller before executing if called from the agent.

### Tool Registration

- [x] Register all tools (`get_closing_tasks`, `get_task_dependencies`, `get_period_status`, `get_closing_config`, `update_closing_config`) in `assets/financial-closing-advisor-agent/app/agent.py` by adding them to the tools list loaded via `get_mcp_tools()` or alongside it. Since there are no MCP servers (no available external APIs), load these local tools directly in `agent.py` as the agent's tool set.
  - Use LangChain `StructuredTool.from_function()` for each tool.
  - Wire the tool list into the agent graph as the complete tool set.

---

## Business Instrumentation

- [x] Implement business step instrumentation for all 5 milestones from the PRD:

  - **M1 — Closing Status Retrieved**: emit `M1.achieved: closing task status retrieved for active period — <task_count> tasks returned` on success; `M1.missed: closing task status retrieval failed — AFC unavailable or no active period found` on failure.

  - **M2 — Dependency Chain Evaluated**: emit `M2.achieved: dependency chain evaluated — critical path identified, <blocked_count> blocked tasks surfaced` on success; `M2.missed: dependency chain evaluation incomplete — insufficient task metadata or dependency data unavailable` on failure.

  - **M3 — Prioritised Action List Generated**: emit `M3.achieved: prioritised action list generated — <action_count> recommended actions returned` on success; `M3.missed: action list generation failed — dependency evaluation or status data incomplete` on failure.

  - **M4 — Blocker Resolved (Root Cause Identified)**: emit `M4.achieved: root cause identified for blocked task <task_id> — corrective action suggested` on success; `M4.missed: root cause analysis inconclusive for task <task_id> — insufficient error context or upstream data missing` on failure.

  - **M5 — Deadline Alert Triggered**: emit `M5.achieved: deadline alert triggered for task <task_id> — <hours_remaining>h remaining, owner <owner_id> notified` on success; `M5.missed: deadline alert not triggered — configuration missing for entity or threshold not set` on failure.

- [x] Add OpenTelemetry custom spans for each milestone using the decorator form (`@tracer.start_as_current_span("name")`) on plain async helper methods. Extract business logic from `stream()` into a `_run_agent()` async helper to avoid `GeneratorExit` context errors.
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`.

---

## MCP Tool Integration

No external MCP servers are available (all AFC APIs are unavailable in this landscape). The agent uses local tool implementations instead. Skip Path A and Path B MCP wiring.

- [x] Ensure `asset.yaml` has no `requires` entries pointing to unavailable MCP servers. The agent's tools are all local.
- [x] Since there are no MCP spec files and no translation files, skip `mcp-mock-config` generation for external MCP servers. Instead, create `assets/financial-closing-advisor-agent/mcp-mock.json` manually with mock responses for all 5 local tools using the format expected by `conftest.py`. Each tool entry must have a `mock_response` with realistic test data matching the mock data store.

---

## Testing

- [x] Write unit tests in `assets/financial-closing-advisor-agent/tests/`:
  - `test_get_closing_tasks.py` — verify the tool returns the expected list of tasks with correct fields; assert at least one blocked, one in-progress, and one completed task are present.
  - `test_get_task_dependencies.py` — verify the dependency map is returned; assert that tasks with declared dependencies reference valid task_ids.
  - `test_get_period_status.py` — verify the tool returns a dict with `period`, `status`, and `closing_deadline` fields.
  - `test_get_closing_config.py` — verify full config is returned; verify specific section retrieval works.
  - `test_update_closing_config.py` — verify a config parameter can be updated and the updated value is returned in a subsequent `get_closing_config` call.
- [x] Write one integration test `tests/test_agent_integration.py` exercising the end-to-end agent flow: mock the LLM to return a canned response, invoke the agent with "What are the current closing task statuses?", assert the `get_closing_tasks` tool was called and a response containing task status information is returned.
- [x] Run `pytest` from `assets/financial-closing-advisor-agent/` (no args). Fix any failures immediately.
- [x] If coverage < 70%, add targeted tests until threshold is met.
- [x] Run `pytest` again (no args) to generate final `test_report.json`.
- [x] Verify `test_report.json` exists in `assets/financial-closing-advisor-agent/`.
