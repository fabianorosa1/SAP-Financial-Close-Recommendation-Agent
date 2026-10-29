---
name: next-action-recommender
description: Recommends the next financial closing activities in the correct execution sequence with reasoning, based on current task statuses and the dependency chain.
---

# Next Action Recommender

## When to Use This Skill

Load this skill when the user asks what to do next, needs a prioritised action list, or wants to know the correct sequence of tasks to progress the closing cycle.

## Instructions

### Step 1: Retrieve Current State

Call `get_closing_tasks` to get all tasks and their statuses.
Call `get_task_dependencies` to get the dependency map.
Call `get_closing_config` with section `deadline_proximity_alert_hours` to get the alert threshold.

### Step 2: Identify Actionable Tasks

An actionable task is one that is:
- Status: `pending`
- All upstream dependencies have status `completed`

Filter the full task list to actionable tasks only.

### Step 3: Prioritise Actionable Tasks

Apply the prioritisation rules from `references/prioritisation-rules.md`:
1. Deadline proximity (tasks breaching soonest come first)
2. Task priority level (high > medium > low)
3. Dependency chain depth (tasks that unblock more downstream tasks rank higher)

### Step 4: Build the Action List

For each actionable task (in priority order), return:
- Task ID and description
- Owner (who should action it)
- Deadline
- Justification: why this task is recommended now (e.g., "High priority — deadline in 3 hours; unblocks 4 downstream tasks")
- Recommended action: a plain-language instruction for the controller

### Step 5: Handle Edge Cases

- If there are no actionable tasks → report which tasks are blocking progress and suggest resolving the top blocker first (see blocker-root-cause-analyzer skill).
- If all tasks are completed → congratulate the controller and confirm the period close is complete.

## Output Format

Return a numbered, ordered list. Each entry: Task ID | Description | Owner | Deadline | Justification | Recommended Action.
