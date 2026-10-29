# Escalation Matrix

## Severity Levels

| Severity | Trigger (remaining time) | Default Threshold | Escalation Action |
|----------|--------------------------|-------------------|-------------------|
| Warning  | ≤ warning_hours          | 8 hours           | Notify task owner directly. Include task details and deadline. Request confirmation that the task is in progress. |
| Critical | ≤ critical_hours         | 4 hours           | Notify task owner AND finance lead. Mark as urgent. Request immediate status update and escalation path. |
| Breach   | ≤ breach_hours (0)       | 0 hours (overdue) | Immediate escalation to finance manager. Document the breach. Assess impact on dependent tasks. Initiate incident response if required. |

## Escalation Message Template

For each alert:
```
[SEVERITY] Deadline Alert — Task [task_id]: [task_description]
Owner: [owner_name] <[owner_email]>
Remaining Time: [X hours Y minutes]
Deadline: [deadline formatted]
Recommended Action: [action from severity level above]
```
