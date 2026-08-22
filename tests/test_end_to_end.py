from solstice.app_state import kiosk_service, queue_service
from solstice.checkin_service import CheckInService


kiosk = kiosk_service
queue = queue_service

service = CheckInService(
    kiosk_service=kiosk,
    queue_service=queue,
)


print("=" * 60)
print("SOLSTICE END-TO-END CHECK-IN TEST")
print("=" * 60)


# Scan attendee
result = service.scan_and_queue("ATT-001")

print("\n--- SCAN ---")
print("Accepted:", result["accepted"])
print("Reason:", result["reason"])
print("Request ID:", result["request_id"])
print("Status:", result["attendee"].status.value)


assert result["accepted"] is True
assert result["reason"] == "PRINT_REQUEST_QUEUED"
assert result["attendee"].status.value == "PENDING"


print("\nWaiting for vendor + webhook...")
print("The vendor simulator should now process the request.")


print("\n" + "=" * 60)
print("SCAN SUCCESSFULLY QUEUED")
print("=" * 60)