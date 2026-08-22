import json

import pika


RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
QUEUE_NAME = "badge.print.requests"


class QueueService:
    def __init__(
        self,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        queue_name=QUEUE_NAME,
    ):
        self.host = host
        self.port = port
        self.queue_name = queue_name

    def publish_print_request(self, attendee_id, request_id, attendee_name):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
            )
        )

        try:
            channel = connection.channel()

            channel.queue_declare(
                queue=self.queue_name,
                durable=True,
            )

            message = {
                "attendee_id": attendee_id,
                "request_id": request_id,
                "attendee_name": attendee_name,
            }

            channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent,
                    content_type="application/json",
                ),
            )

            return message

        finally:
            connection.close()