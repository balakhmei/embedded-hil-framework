"""Small, hardware-independent models used to validate the project scaffold."""
from dataclasses import dataclass
from enum import Enum

class RunOutcome(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    INFRASTRUCTURE_ERROR = "infrastructure_error"

@dataclass(frozen=True)
class ResultRecord:
    name: str
    outcome: RunOutcome
    details: str = ""
