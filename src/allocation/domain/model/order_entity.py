from datetime import datetime
from dataclasses import dataclass


class OrderItem:
    def __init__(self, created_at: datetime,
                 order_id: int,
                 price_usd: float,
                 cogs_usd: float,
                 website_session_id: int,
                 product_id: int,
                 is_primary_item: bool):

        self.order_id = order_id
        self.product_id = product_id
        self.website_session_id = website_session_id
        self.cogs_usd = cogs_usd
        self.price_usd = price_usd
        self.created_at = created_at
        self.is_primary_item = is_primary_item

    def __repr__(self) -> str:
        return "Product: {}, price_usd: {}, at: {} ".format(self.product_id, self.price_usd, self.created_at)

    def add(self, session):
        session.add(self)

    def get(self, session, item_order_id):
        return session.query(OrderItem).filter_by(id=item_order_id)

    def remove(self, session):
        session.delete(self)

    def value(self) -> float:
        return self.price_usd

    def is_prime(self) -> bool:
        return self.is_primary_item


"""
@dataclass(unsafe_hash=True)
class OrderItemRefund:
    order_item_id: str
    created_at: datetime
    order_item_id: int
    order_id: int
    refund_amount_usd: float
"""