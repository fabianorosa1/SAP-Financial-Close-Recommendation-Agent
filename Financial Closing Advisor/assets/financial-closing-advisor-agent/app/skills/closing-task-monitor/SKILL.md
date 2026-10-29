---
name: closing-task-monitor
description: Retrieves and presents the status of all financial closing tasks for the active period, including status, owner, priority, and deadline.
---

# Closing Task Monitor

## When to Use This Skill

Load this skill when the user asks about the current status of closing tasks, wants a summary of the period-end close progress, or needs to know which tasks are completed, in-progress, blocked, or pending.

## Instructions

### Step 1: Retrieve All Closing Tasks

Call the `get_closing_tasks` tool to retrieve all tasks for the active period. If a period is specified by the user, pass it as the `period` parameter.

### Step 2: Classify Each Task

Classify each task using the definitions in `references/task-status-definitions.md`.

### Step 3: Build a Structured Summary

Return a structured summary with the following for each task:
- Task ID and description
- Status (completed / in-progress / blocked / pending)
- Owner (name and email if available)
- Priority (high / medium / low)
- Deadline (formatted as a human-readable date and time)
- For blocked tasks: include a brief note that a root-cause analysis is available

### Step 4: Provide a High-Level Overview

After the task list, provide a brief overview:
- Total tasks, completed count, in-progress count, blocked count, pending count
- Number of high-priority tasks still open
- Any tasks with deadlines within 8 hours

## Error Handling

If `get_closing_tasks` returns an error or empty result:
1. Report the error message exactly as received.
2. Inform the controller that the closing task status could not be retrieved.
3. Suggest checking the period parameter or contacting the AFC system administrator.
