"""
Mock closing task store simulating SAP Advanced Financial Closing (AFC) task data.
Returns a static list of realistic month-end closing tasks.
"""
from datetime import datetime, timezone, timedelta
from typing import Optional


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_closing_tasks(period: Optional[str] = None) -> list[dict]:
    """
    Returns all closing tasks for the active (or specified) period.
    Each task includes: task_id, description, status, owner, priority,
    deadline, dependencies, error_message (optional), missing_fields (optional).
    """
    base = _now()

    tasks = [
        {
            "task_id": "T001",
            "description": "Accounts Payable Reconciliation",
            "status": "completed",
            "owner": {"name": "Alice Chen", "email": "alice.chen@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=24)).isoformat(),
            "dependencies": [],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T002",
            "description": "Accounts Receivable Clearing",
            "status": "completed",
            "owner": {"name": "Bob Kumar", "email": "bob.kumar@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=24)).isoformat(),
            "dependencies": [],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T003",
            "description": "Fixed Asset Depreciation Run",
            "status": "in-progress",
            "owner": {"name": "Carol Smith", "email": "carol.smith@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=6)).isoformat(),
            "dependencies": [],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T004",
            "description": "Inventory Valuation",
            "status": "blocked",
            "owner": {"name": "David Lee", "email": "david.lee@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=8)).isoformat(),
            "dependencies": ["T001"],
            "error_message": "PERIOD_NOT_OPEN: Financial period 2024-12 is not open for posting in company code 1000.",
            "missing_fields": [],
        },
        {
            "task_id": "T005",
            "description": "Intercompany Eliminations",
            "status": "blocked",
            "owner": {"name": "Emma Wilson", "email": "emma.wilson@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=3)).isoformat(),
            "dependencies": ["T001", "T002"],
            "error_message": "INCOMPLETE_INTERCOMPANY_POSTING: Counterpart posting missing for company code 2000.",
            "missing_fields": [],
        },
        {
            "task_id": "T006",
            "description": "Foreign Currency Revaluation",
            "status": "blocked",
            "owner": {"name": "Frank Müller", "email": "frank.muller@company.com"},
            "priority": "medium",
            "deadline": (base + timedelta(hours=10)).isoformat(),
            "dependencies": ["T001", "T002"],
            "error_message": None,
            "missing_fields": ["exchange_rate_EUR_USD_2024-12-31", "exchange_rate_GBP_USD_2024-12-31"],
        },
        {
            "task_id": "T007",
            "description": "Accruals Posting",
            "status": "pending",
            "owner": {"name": "Grace Tanaka", "email": "grace.tanaka@company.com"},
            "priority": "medium",
            "deadline": (base + timedelta(hours=12)).isoformat(),
            "dependencies": ["T001", "T002"],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T008",
            "description": "Cost Centre Allocation",
            "status": "pending",
            "owner": {"name": "Henry Brown", "email": "henry.brown@company.com"},
            "priority": "medium",
            "deadline": (base + timedelta(hours=14)).isoformat(),
            "dependencies": ["T003", "T007"],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T009",
            "description": "Profit Centre Settlement",
            "status": "pending",
            "owner": {"name": "Irene Patel", "email": "irene.patel@company.com"},
            "priority": "medium",
            "deadline": (base + timedelta(hours=16)).isoformat(),
            "dependencies": ["T008"],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T010",
            "description": "Trial Balance Extraction",
            "status": "pending",
            "owner": {"name": "James O'Brien", "email": "james.obrien@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=18)).isoformat(),
            "dependencies": ["T001", "T002", "T003", "T004", "T005", "T006", "T007", "T008", "T009"],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T011",
            "description": "Management Report Generation",
            "status": "pending",
            "owner": {"name": "Karen Liu", "email": "karen.liu@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=5)).isoformat(),
            "dependencies": ["T010"],
            "error_message": None,
            "missing_fields": [],
        },
        {
            "task_id": "T012",
            "description": "Period Lock",
            "status": "pending",
            "owner": {"name": "Alice Chen", "email": "alice.chen@company.com"},
            "priority": "high",
            "deadline": (base + timedelta(hours=22)).isoformat(),
            "dependencies": ["T010", "T011"],
            "error_message": None,
            "missing_fields": [],
        },
    ]

    return tasks


def get_active_period() -> str:
    """Returns the active closing period identifier."""
    now = _now()
    return f"{now.year}-{now.month:02d}"
