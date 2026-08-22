from solstice.app_state import kiosk_service
from solstice.webhook_service import create_webhook_app


app = create_webhook_app(kiosk_service)


if __name__ == "__main__":
    print("Solstice Webhook Server")
    print("Webhook: http://127.0.0.1:5000/webhooks/print-completed")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )