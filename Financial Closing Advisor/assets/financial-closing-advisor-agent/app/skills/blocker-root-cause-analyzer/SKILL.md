---
name: blocker-root-cause-analyzer
description: Identifies the root cause of a blocked closing task (missing data, incomplete upstream task, system error, or configuration issue) and suggests a corrective action the financial controller can execute.
---

# Blocker Root Cause Analyzer

## When to Use This Skill

Load this skill when the user asks why a task is blocked, needs to understand the root cause of a failure, or wants corrective action suggestions for a specific blocked task.

## Instructions

### Step 1: Retrieve Task Details

Call `get_closing_tasks` and find the specified blocked task by task_id.
Call `get_task_dependencies` to get the dependency map.

### Step 2: Classify the Root Cause

Apply the decision tree below in order:

#### Case 1: Upstream Dependency Incomplete
- Check if any of the task's dependencies have status `pending`, `in-progress`, or `blocked`.
- If yes → root cause is "Upstream task not completed".
- Corrective action: "Complete or resolve upstream task [task_id]: [task_description] before actioning this task."

#### Case 2: System Error
- Check if the task has a non-empty `error_message` field.
- If yes → root cause is "System error during task execution".
- Corrective action: "Review the system error: [error_message]. Options: (1) Re-run the task after verifying the system is operational. (2) Contact the system administrator if the error persists. (3) Check the error patterns reference for known resolutions."
- See `references/error-patterns.md` for known error patterns and resolutions.

#### Case 3: Missing Required Data
- Check if the task has a non-empty `missing_fields` list.
- If yes → root cause is "Required data not provided".
- Corrective action: "Provide the following required fields before re-running: [list each field and its data owner if known]."

#### Case 4: Configuration Missing
- If none of the above → root cause is likely a missing configuration parameter.
- Corrective action: "Check the closing configuration for this entity and period. Use the 'get_closing_config' tool to review current configuration and 'update_closing_config' to add any missing parameters."

### Step 3: Return Root Cause Report

Return:
- Task ID and description
- Root cause category (one of: Upstream Dependency, System Error, Missing Data, Configuration)
- Root cause explanation (specific details)
- Corrective action (step-by-step, actionable)
- Estimated effort: Low (< 30 min) / Medium (30 min – 2 hours) / High (> 2 hours)

## Error Handling

If the task is not found or is not in blocked status, inform the user and suggest calling the closing-task-monitor skill to get current statuses.
