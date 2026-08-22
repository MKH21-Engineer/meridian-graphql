Original synchronous architecture:
Staff scan → REST print API → wait → Checked In

Solstice asynchronous architecture:
Staff scan
→ duplicate/state validation
→ RabbitMQ print request
→ vendor simulator
→ badge printing
→ signed webhook
→ CHECKED_IN