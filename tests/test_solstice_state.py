from solstice.kiosk_service import KioskService
from solstice.models import AttendeeStatus


service = KioskService()


# --------------------------------------------------
# 1. ATT-001: normal scan
# --------------------------------------------------

result = service.scan_attendee("ATT-001")

assert result["accepted"] is True
assert result["attendee"].status == AttendeeStatus.PENDING

request_id = result["request_id"]

print("\n--- ATT-001 SCAN ---")
print("Accepted:", result["accepted"])
print("Request ID:", request_id)
print("Status:", result["attendee"].status.value)


# --------------------------------------------------
# 2. ATT-001: valid webhook
# --------------------------------------------------

webhook = service.handle_print_webhook(
    "ATT-001",
    request_id,
)

assert webhook["accepted"] is True
assert webhook["reason"] == "CHECK_IN_CONFIRMED"
assert webhook["attendee"].status == AttendeeStatus.CHECKED_IN

print("\n--- ATT-001 VALID WEBHOOK ---")
print("Accepted:", webhook["accepted"])
print("Reason:", webhook["reason"])
print("Status:", webhook["attendee"].status.value)


# --------------------------------------------------
# 3. ATT-001: duplicate webhook
# --------------------------------------------------

duplicate_webhook = service.handle_print_webhook(
    "ATT-001",
    request_id,
)

assert duplicate_webhook["accepted"] is True
assert duplicate_webhook["reason"] == "ALREADY_CHECKED_IN"
assert duplicate_webhook["attendee"].status == AttendeeStatus.CHECKED_IN

print("\n--- ATT-001 DUPLICATE WEBHOOK ---")
print("Accepted:", duplicate_webhook["accepted"])
print("Reason:", duplicate_webhook["reason"])
print("Status:", duplicate_webhook["attendee"].status.value)


# --------------------------------------------------
# 4. ATT-002: stale/out-of-order webhook
# --------------------------------------------------

result_2 = service.scan_attendee("ATT-002")

assert result_2["accepted"] is True

correct_request_id_2 = result_2["request_id"]

stale_request_id = "old-request-that-does-not-match"

stale_webhook = service.handle_print_webhook(
    "ATT-002",
    stale_request_id,
)

assert stale_webhook["accepted"] is False
assert stale_webhook["reason"] == "STALE_OR_OUT_OF_ORDER_REQUEST"
assert stale_webhook["attendee"].status == AttendeeStatus.PENDING

print("\n--- ATT-002 STALE WEBHOOK ---")
print("Accepted:", stale_webhook["accepted"])
print("Reason:", stale_webhook["reason"])
print("Status:", stale_webhook["attendee"].status.value)


# --------------------------------------------------
# 5. ATT-002: correct webhook after stale one
# --------------------------------------------------

correct_webhook_2 = service.handle_print_webhook(
    "ATT-002",
    correct_request_id_2,
)

assert correct_webhook_2["accepted"] is True
assert correct_webhook_2["reason"] == "CHECK_IN_CONFIRMED"
assert correct_webhook_2["attendee"].status == AttendeeStatus.CHECKED_IN

print("\n--- ATT-002 CORRECT WEBHOOK ---")
print("Accepted:", correct_webhook_2["accepted"])
print("Reason:", correct_webhook_2["reason"])
print("Status:", correct_webhook_2["attendee"].status.value)


# --------------------------------------------------
# 6. ATT-003: duplicate scan protection
# --------------------------------------------------

result_3 = service.scan_attendee("ATT-003")

assert result_3["accepted"] is True

duplicate_scan = service.scan_attendee("ATT-003")

assert duplicate_scan["accepted"] is False
assert duplicate_scan["attendee"].status == AttendeeStatus.PENDING

print("\n--- ATT-003 DUPLICATE SCAN ---")
print("Accepted:", duplicate_scan["accepted"])
print("Reason:", duplicate_scan["reason"])
print("Status:", duplicate_scan["attendee"].status.value)


print("\n" + "=" * 50)
print("✅ ALL SOLSTICE STATE-MACHINE TESTS PASSED")
print("=" * 50)