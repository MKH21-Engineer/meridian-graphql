from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AttendeeStatus(Enum):
    NOT_CHECKED_IN = "NOT_CHECKED_IN"
    PENDING = "PENDING"
    CHECKED_IN = "CHECKED_IN"


@dataclass
class Attendee:
    attendee_id: str
    name: str
    status: AttendeeStatus = AttendeeStatus.NOT_CHECKED_IN
    active_request_id: Optional[str] = None