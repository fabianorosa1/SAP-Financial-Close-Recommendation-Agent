# Task Prioritisation Rules

## Primary: Deadline Proximity

Sort actionable tasks by remaining time to deadline (ascending — soonest deadline first).

| Remaining Time | Priority Band |
|----------------|---------------|
| < 4 hours      | Critical       |
| 4–8 hours      | Warning        |
| > 8 hours      | Normal         |

Always surface critical-band tasks at the top of the action list regardless of other criteria.

## Secondary: Task Priority Level

Within the same deadline proximity band, sort by the task's declared priority:
1. high
2. medium
3. low

## Tertiary: Dependency Chain Depth

Within the same priority band and level, prefer tasks that unblock more downstream tasks. A task that is a prerequisite for 5 other tasks ranks higher than one that is a prerequisite for 1.

## Tiebreaker

If all criteria are equal, sort alphabetically by task_id.
