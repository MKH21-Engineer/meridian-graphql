import hashlib
import hmac
import json

from solstice.kiosk_service import KioskService
from solstice.webhook_service import create_webhook_app, WEBHOOK_SECRET


kiosk = KioskService()
app = create_webhook_app(kiosk)
client = app.test_client()


# Put ATT-001 into PENDING state first
scan_result = kiosk.scan_attendee("ATT-001")

request_id = scan_result["request_id"]


payload = {
    "attendee_id": "ATT-001",
    "request_id": request_id,
}


raw_body = json.dumps(payload).encode()

signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    raw_body,
    hashlib.sha256,
).hexdigest()


response = client.post(
    "/webhooks/print-completed",
    data=raw_body,
    content_type="application/json",
    headers={
        "X-Solstice-Signature": signature,
    },
)


print("Webhook response:")
print(response.status_code)
print(response.json)

print()
print("Attendee status:")
print(kiosk.attendees["ATT-001"].status.value)


assert response.status_code == 200
assert response.json["accepted"] is True
assert response.json["reason"] == "CHECK_IN_CONFIRMED"
assert kiosk.attendees["ATT-001"].status.value == "CHECKED_IN"

print()
print("=" * 50)
print("✅ WEBHOOK TEST PASSED")
print("=" * 50)