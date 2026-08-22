from uuid import uuid4

from .models import Attendee, AttendeeStatus


class KioskService:
    def __init__(self):
        self.attendees = {
            "ATT-001": Attendee("ATT-001", "Alice"),
            "ATT-002": Attendee("ATT-002", "Brian"),
            "ATT-003": Attendee("ATT-003", "Charlie"),
        }

    def scan_attendee(self, attendee_id):
        attendee = self.attendees.get(attendee_id)

        if attendee is None:
            raise ValueError(f"Unknown attendee: {attendee_id}")

        # Duplicate protection
        if attendee.status in (
            AttendeeStatus.PENDING,
            AttendeeStatus.CHECKED_IN,
        ):
            return {
                "accepted": False,
                "reason": "ATTENDEE_ALREADY_PROCESSING_OR_CHECKED_IN",
                "attendee": attendee,
            }

        request_id = str(uuid4())

        attendee.status = AttendeeStatus.PENDING
        attendee.active_request_id = request_id

        return {
            "accepted": True,
            "request_id": request_id,
            "attendee": attendee,
        }

    def handle_print_webhook(self, attendee_id, request_id):
        attendee = self.attendees.get(attendee_id)

        if attendee is None:
            return {
                "accepted": False,
                "reason": "UNKNOWN_ATTENDEE",
            }

        # Ignore callbacks that do not belong to the
        # attendee's currently active print request.
        if attendee.active_request_id != request_id:
            return {
                "accepted": False,
                "reason": "STALE_OR_OUT_OF_ORDER_REQUEST",
                "attendee": attendee,
            }

        # Make repeated webhook deliveries harmless.
        if attendee.status == AttendeeStatus.CHECKED_IN:
            return {
                "accepted": True,
                "reason": "ALREADY_CHECKED_IN",
                "attendee": attendee,
            }

        if attendee.status != AttendeeStatus.PENDING:
            return {
                "accepted": False,
                "reason": "INVALID_STATE",
                "attendee": attendee,
            }

        attendee.status = AttendeeStatus.CHECKED_IN

        return {
            "accepted": True,
            "reason": "CHECK_IN_CONFIRMED",
            "attendee": attendee,
        }