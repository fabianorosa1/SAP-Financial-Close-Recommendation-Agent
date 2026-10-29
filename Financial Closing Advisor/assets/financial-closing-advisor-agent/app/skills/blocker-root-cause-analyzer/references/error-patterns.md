# Common AFC Error Patterns and Resolutions

## PERIOD_NOT_OPEN
**Meaning:** The financial period is not open for posting.
**Resolution:** Check the period status using `get_period_status`. If the period should be open, contact the finance system administrator to open the period for posting.

## MISSING_EXCHANGE_RATE
**Meaning:** Foreign currency revaluation cannot proceed because an exchange rate is missing for the required currency pair and date.
**Resolution:** Maintain the required exchange rate in the system (e.g., transaction OB08 in S/4HANA). Re-run the task after the rate is available.

## INCOMPLETE_INTERCOMPANY_POSTING
**Meaning:** Intercompany elimination cannot complete because a matching posting from the counterpart company is missing.
**Resolution:** Coordinate with the controller responsible for the counterpart company code to ensure their intercompany posting is complete.

## DOCUMENT_LOCKED
**Meaning:** A financial document required by this task is locked by another user or process.
**Resolution:** Wait for the lock to be released, or contact the user/process holding the lock. If the lock is stale, contact the system administrator to release it.

## ALLOCATION_CYCLE_ERROR
**Meaning:** Cost centre allocation cycle failed due to a configuration error in the allocation rules.
**Resolution:** Review the allocation cycle configuration. Verify sender/receiver cost centres and allocation rules are correctly maintained.

## ASSET_NOT_CAPITALISED
**Meaning:** An asset expected to be capitalised by this period is still under construction (AuC) and has not been settled.
**Resolution:** Ensure the investment order or WBS element for the asset has been settled before running the depreciation run.

## BATCH_JOB_FAILED
**Meaning:** A background batch job associated with this task failed.
**Resolution:** Check the batch job log for the specific error. Common causes: authorisation failures, timeout, locked tables. Re-schedule after resolving the underlying cause.
