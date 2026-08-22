import hashlib
import hmac
import json

from flask import Flask, jsonify, request


WEBHOOK_SECRET = "solstice-demo-secret"


def create_webhook_app(kiosk_service):
    app = Flask(__name__)

    @app.post("/webhooks/print-completed")
    def print_completed():
        signature = request.headers.get("X-Solstice-Signature", "")

        raw_body = request.get_data()

        expected_signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            raw_body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return jsonify({
                "accepted": False,
                "reason": "INVALID_SIGNATURE",
            }), 401

        payload = request.get_json(silent=True)

        if not payload:
            return jsonify({
                "accepted": False,
                "reason": "INVALID_JSON",
            }), 400

        result = kiosk_service.handle_print_webhook(
            attendee_id=payload["attendee_id"],
            request_id=payload["request_id"],
        )

        return jsonify({
            "accepted": result["accepted"],
            "reason": result["reason"],
        }), 200

    return app