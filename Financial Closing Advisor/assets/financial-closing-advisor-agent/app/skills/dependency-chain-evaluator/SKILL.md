---
name: dependency-chain-evaluator
description: Evaluates the task dependency chain for the current closing plan, identifies the critical path, and surfaces blocked and at-risk tasks with their upstream dependency context.
---

# Dependency Chain Evaluator

## When to Use This Skill

Load this skill when the user asks about task dependencies, wants to understand the critical path, or needs to know which tasks are blocked by upstream activities.

## Instructions

### Step 1: Retrieve Task List and Dependency Map

Call `get_closing_tasks` to get all tasks and their statuses.
Call `get_task_dependencies` to get the dependency map (which tasks must complete before others can start).

### Step 2: Build the Dependency Graph

For each task, determine:
- Which tasks it depends on (upstream dependencies)
- Which tasks depend on it (downstream tasks)
- Whether all its upstream dependencies are completed

### Step 3: Identify the Critical Path

The critical path is the longest chain of dependent tasks from start to close. To identify it:
1. Find all tasks with no dependencies (root tasks).
2. For each root task, trace forward through the dependency chain.
3. The longest chain (by deadline proximity and task count) is the critical path.

### Step 4: Surface Blocked and At-Risk Tasks

For each blocked task:
- Identify which specific upstream dependency is incomplete or errored.
- Annotate the blocked task with: `blocked_by: <task_id> - <task_description>`.

For each pending task:
- If all upstream dependencies are complete → mark as `actionable now`.
- If any upstream dependency is incomplete → mark as `waiting on <task_id>`.

### Step 5: Return Structured Output

Return:
1. The critical path as an ordered list of task IDs and descriptions.
2. A list of blocked tasks with their upstream dependency noted.
3. A list of currently actionable tasks (pending tasks with all dependencies met).
4. A summary: "X tasks on critical path, Y blocked, Z actionable now."

## Error Handling

If dependency data is unavailable, inform the user and provide guidance based on the task list alone (surface blocked tasks without full chain analysis).
