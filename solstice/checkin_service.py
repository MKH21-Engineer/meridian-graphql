from solstice.kiosk_service import KioskService
from solstice.queue_service import QueueService
from solstice.models import AttendeeStatus


class CheckInService:
    def __init__(self, kiosk_service=None, queue_service=None):
        self.kiosk_service = kiosk_service or KioskService()
        self.queue_service = queue_service or QueueService()

    def scan_and_queue(self, attendee_id):
        result = self.kiosk_service.scan_attendee(attendee_id)

        # Unknown attendee or duplicate scan
        if not result["accepted"]:
            return result

        attendee = result["attendee"]
        request_id = result["request_id"]

        try:
            message = self.queue_service.publish_print_request(
                attendee_id=attendee.attendee_id,
                request_id=request_id,
                attendee_name=attendee.name,
            )

        except Exception as exc:
            # Roll back PENDING if RabbitMQ publishing fails
            attendee.status = AttendeeStatus.NOT_CHECKED_IN
            attendee.active_request_id = None

            return {
                "accepted": False,
                "reason": "PRINT_REQUEST_PUBLISH_FAILED",
                "error": str(exc),
                "attendee": attendee,
            }

        return {
            "accepted": True,
            "reason": "PRINT_REQUEST_QUEUED",
            "request_id": request_id,
            "message": message,
            "attendee": attendee,
        }