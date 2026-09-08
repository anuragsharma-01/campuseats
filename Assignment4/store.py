class OrderStore:
    def __init__(self):
        self.orders = {}
        self.idempotency = {}

    def save(self, order): self.orders[order.id] = order
    def get(self, order_id): return self.orders.get(order_id)
    def list(self, status=None):
        xs=list(self.orders.values())
        return [x for x in xs if not status or x.status == status]
    def remember(self, key, order_id): self.idempotency[key] = order_id
    def existing(self, key): return self.idempotency.get(key)
