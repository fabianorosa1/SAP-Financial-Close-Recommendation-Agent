# Task Status Definitions

## completed
The task has been successfully executed and all required outputs have been produced. No further action is needed on this task.

## in-progress
The task has been started and is currently being processed. It is not yet complete but is not blocked. Monitor for completion against the deadline.

## blocked
The task cannot proceed. A blocker exists — this may be:
- An upstream dependency task that is not yet completed
- A system error that occurred during task execution
- Missing required data fields that have not been provided
- A missing configuration parameter

For blocked tasks, always indicate that a root-cause analysis is available via the blocker-root-cause-analyzer skill.

## pending
The task has not yet started. It is waiting to be actioned. A pending task may be actionable now (if all dependencies are complete) or waiting on upstream tasks.
