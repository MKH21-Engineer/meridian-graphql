import hashlib
import hmac
import json
import time

import pika
import requests


RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
QUEUE_NAME = "badge.print.requests"

WEBHOOK_URL = "http://localhost:5000/webhooks/print-completed"
WEBHOOK_SECRET = "solstice-demo-secret"


class VendorSimulator:
    def __init__(
        self,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        queue_name=QUEUE_NAME,
    ):
        self.host = host
        self.port = port
        self.queue_name = queue_name

    def start(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
            )
        )

        channel = connection.channel()

        channel.queue_declare(
            queue=self.queue_name,
            durable=True,
        )

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._handle_message,
        )

        print("Solstice Vendor Simulator")
        print(f"Listening on queue: {self.queue_name}")
        print("Waiting for badge print requests...")

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("\nVendor simulator stopped.")
        finally:
            connection.close()

    def _handle_message(self, channel, method, properties, body):
        message = json.loads(body)

        print("\n--- PRINT REQUEST RECEIVED ---")
        print(f"Attendee: {message['attendee_name']}")
        print(f"Attendee ID: {message['attendee_id']}")
        print(f"Request ID: {message['request_id']}")

        print("Printing badge...")
        time.sleep(2)

        print("Badge printed successfully.")

        # Send completion callback to Solstice
        payload = {
            "attendee_id": message["attendee_id"],
            "request_id": message["request_id"],
        }

        raw_body = json.dumps(payload).encode()

        signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            raw_body,
            hashlib.sha256,
        ).hexdigest()

        response = requests.post(
            WEBHOOK_URL,
            data=raw_body,
            headers={
                "Content-Type": "application/json",
                "X-Solstice-Signature": signature,
            },
            timeout=10,
        )

        print(f"Webhook response: {response.status_code}")
        print(response.json())

        channel.basic_ack(
            delivery_tag=method.delivery_tag
        )


if __name__ == "__main__":
    VendorSimulator().start()