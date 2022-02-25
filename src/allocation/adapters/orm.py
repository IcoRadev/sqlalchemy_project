from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.indexable import index_property
from sqlalchemy.orm import relationship, registry, mapper
from allocation.domain.model import chat_session_entity, order_entity, website_entity
from allocation.domain import batch_entity
from allocation import config

cfg = config.get_configuration()

engine = create_engine(cfg["url"])
metadata = MetaData()
mapper_registry = registry(metadata)


@mapper_registry.mapped
class OrderItem:
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    order_id = Column(Integer, index=True)
    price_usd = Column(Float)
    cogs_usd = Column(Float)
    website_session_id = Column(Integer, ForeignKey("website_sessions.id"))
    product_id = Column(Integer, nullable=False)
    is_primary_item = Column(Boolean)

    index = index_property("user_id", Integer)
    website_sessions = relationship("WebsiteSession", back_populates="order_item")
    order_item_refunds = relationship("OrderItemRefund", back_populates="order_item")
    order_item_refunds_orders = relationship("OrderItemRefund", back_populates="order_items_order")
    chat_sessions = relationship("ChatSession", back_populates="order_item")


@mapper_registry.mapped
class OrderItemRefund:
    __tablename__ = "order_item_refunds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    order_item_id = Column(Integer, ForeignKey("order_items.id"))
    order_id = Column(Integer, ForeignKey("order_items.order_id"))
    refund_amount_usd = Column(Float, nullable=False)

    order_item = relationship("OrderItem", back_populates="order_item_refunds")
    order_items_order = relationship("OrderItem", back_populates="order_item_refunds_orders")


@mapper_registry.mapped
class ChatSession:
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    representative_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("website_sessions.user_id"))
    website_session_id = Column(Integer, ForeignKey("website_sessions.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    children = relationship("ChatAllocation", cascade="all,delete", backref="ChatSession")
    chat_allocations = relationship("ChatAllocation", back_populates="chat_session")
    order_item = relationship("OrderItem", back_populates="chat_sessions")
    website_session = relationship("WebsiteSession", back_populates="chat_sessions")
    website_session_user = relationship("WebsiteSession", back_populates="chat_session_users")


@mapper_registry.mapped
class WebsiteSession:
    __tablename__ = "website_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    user_id = Column(Integer, index=True)
    is_repeat_session = Column(Boolean)
    utm_source = Column(String(128))
    utm_campaign = Column(String(128))
    utm_content = Column(String(128))
    device_type = Column(String(128))
    http_referer = Column(String(128))

    index = index_property("user_id", Integer)
    order_item = relationship("OrderItem", back_populates="website_sessions")
    chat_sessions = relationship("ChatSession", back_populates="website_session")
    chat_session_users = relationship("ChatSession", back_populates="website_session_user")
    website_pageviews = relationship("WebsitePageview", back_populates="website_session")


@mapper_registry.mapped
class WebsitePageview:
    __tablename__ = "website_pageviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    website_session_id = Column(Integer, ForeignKey("website_sessions.id"))
    pageview_url = Column(String(128))

    website_session = relationship("WebsiteSession", back_populates="website_pageviews")


@mapper_registry.mapped
class Batch:
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_type = Column(String(128))
    tag = Column(String(128), index=True)

    index = index_property("batch_tag", Integer)
    children = relationship("ChatAllocation", cascade="all,delete", backref="Batch")
    chat_allocations = relationship("ChatAllocation", back_populates="")


@mapper_registry.mapped
class ChatAllocation:
    __tablename__ = "chat_allocations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_tag = Column(String(128), ForeignKey("batches.tag"))
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"))

    chat_session = relationship("ChatSession", back_populates="chat_allocations")
    batch_entity = relationship("Batch", back_populates="chat_allocations")


def start_mappers():
    # Entities
    mapper(order_entity.OrderItem, OrderItem)
    mapper(website_entity.WebsiteSession, WebsiteSession)
    chat_mapper = mapper(chat_session_entity.ChatSession, ChatSession)
    # Batches
    chat_allocations = mapper(chat_session_entity.ChatAllocation, ChatAllocation)
    mapper(batch_entity.Batch, Batch)
    #
    # batches_mapper = mapper(batch_entity.Batch, Batch,
    #                         properties={
    #                             "chat_allocations": relationship(
    #                                 chat_mapper,
    #                                 secondary=chat_allocations)})

    metadata.create_all(bind=engine)
