from datetime import datetime
from allocation.domain.model.root_entity import Entity


class OrderItem(Entity):
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

    def __enter__(self):
        super().__init__()

    def is_prime(self) -> bool:
        return self.is_primary_item

    @classmethod
    def add(cls, session):
        session.add(cls)

    @classmethod
    def remove(cls, session, entity_id):
        entity = session.query(cls).filter(cls.id == entity_id).first()
        session.delete(entity)

    @classmethod
    def get(cls, session, entity_id):
        entity = session.query(cls).filter(cls.id == entity_id).first()
        return entity.__repr__()

    @classmethod
    def list(cls, session, entity: object):
        return session.query(entity).all()


"""
@dataclass(unsafe_hash=True)
class OrderItemRefund:
    order_item_id: str
    created_at: datetime
    order_item_id: int
    order_id: int
    refund_amount_usd: float
"""