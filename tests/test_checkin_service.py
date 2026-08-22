from solstice.checkin_service import CheckInService
from solstice.kiosk_service import KioskService


class FakeQueueService:
    def __init__(self):
        self.messages = []

    def publish_print_request(
        self,
        attendee_id,
        request_id,
        attendee_name,
    ):
        message = {
            "attendee_id": attendee_id,
            "request_id": request_id,
            "attendee_name": attendee_name,
        }

        self.messages.append(message)

        return message


kiosk = KioskService()
queue = FakeQueueService()

service = CheckInService(
    kiosk_service=kiosk,
    queue_service=queue,
)


# First scan
result = service.scan_and_queue("ATT-001")

print("--- FIRST SCAN ---")
print(result)
print("Status:", kiosk.attendees["ATT-001"].status.value)


assert result["accepted"] is True
assert result["reason"] == "PRINT_REQUEST_QUEUED"
assert kiosk.attendees["ATT-001"].status.value == "PENDING"
assert len(queue.messages) == 1


# Duplicate scan
duplicate = service.scan_and_queue("ATT-001")

print()
print("--- DUPLICATE SCAN ---")
print(duplicate)
print("Status:", kiosk.attendees["ATT-001"].status.value)


assert duplicate["accepted"] is False
assert duplicate["reason"] == "ATTENDEE_ALREADY_PROCESSING_OR_CHECKED_IN"
assert len(queue.messages) == 1


print()
print("=" * 50)
print("✅ CHECK-IN ORCHESTRATION TEST PASSED")
print("=" * 50)