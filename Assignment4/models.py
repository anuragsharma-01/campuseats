from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Order:
    id: str
    customer_id: str
    restaurant_id: str
    items: list
    status: str
    created_at: str
    delivery_address: str = ""
    internal_payment_reference: str = ""

    def as_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "restaurant_id": self.restaurant_id,
            "items": self.items,
            "delivery_address": self.delivery_address,
            "status": self.status,
            "created_at": self.created_at,
        }

def now_iso():
    return datetime.now(timezone.utc).isoformat()
