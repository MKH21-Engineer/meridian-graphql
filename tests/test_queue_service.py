from solstice.queue_service import QueueService


queue_service = QueueService()

message = queue_service.publish_print_request(
    attendee_id="ATT-001",
    request_id="test-request-001",
    attendee_name="Alice",
)

print("Published message:")
print(message)
print()
print("RABBITMQ QUEUE TEST: OK")