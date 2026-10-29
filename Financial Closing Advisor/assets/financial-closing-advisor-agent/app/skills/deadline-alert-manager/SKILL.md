---
name: deadline-alert-manager
description: Detects tasks approaching their configured deadline proximity threshold and generates escalation alerts identifying the at-risk task, owner, remaining time, and recommended escalation action.
---

# Deadline Alert Manager

## When to Use This Skill

Load this skill when the user wants to check for upcoming deadline breaches, requests a deadline alert scan, or the agent detects tasks with less remaining time than the configured threshold.

## Instructions

### Step 1: Retrieve Configuration and Tasks

Call `get_closing_config` with section `escalation_thresholds` to get the warning, critical, and breach thresholds.
Call `get_closing_config` with section `deadline_proximity_alert_hours` for the general alert window.
Call `get_closing_tasks` to get all open tasks (status: pending, in-progress, blocked).

### Step 2: Calculate Remaining Time

For each open task:
- Parse the `deadline` field (ISO datetime).
- Calculate remaining hours = (deadline - now).
- Ignore completed tasks.

### Step 3: Classify and Generate Alerts

Apply the escalation matrix from `references/escalation-matrix.md`:

| Remaining Time | Severity | Action |
|----------------|----------|--------|
| ≤ breach_hours (0) | Breach | Immediate escalation to finance manager |
| ≤ critical_hours (4) | Critical | Urgent alert to task owner + finance lead |
| ≤ warning_hours (8) | Warning | Alert to task owner |

For each at-risk task (at any severity level), generate an alert containing:
- Task ID and description
- Owner (name and email)
- Remaining time (in hours and minutes)
- Severity level (Warning / Critical / Breach)
- Recommended escalation action

### Step 4: Return Alert Summary

Return all alerts sorted by severity (Breach first, then Critical, then Warning), then by remaining time (soonest first within each severity).

If no tasks are at risk → confirm: "No tasks are approaching their deadline thresholds at this time."

## Error Handling

If configuration is missing for escalation thresholds, use defaults: warning=8h, critical=4h, breach=0h. Inform the user that defaults are being applied and suggest updating the configuration.
