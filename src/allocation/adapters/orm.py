from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.indexable import index_property
from sqlalchemy.orm import relationship, registry, mapper
from allocation.domain.model import chat_session_entity, order_entity, website_entity
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

    order_item = relationship("OrderItem", back_populates="chat_sessions")
    website_session = relationship("WebsiteSession", back_populates="chat_sessions")
    website_session_user = relationship("WebsiteSession", back_populates="chat_session_users")


@mapper_registry.mapped
class WebsiteSession:
    __tablename__ = "website_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    # user_id = Column(Index, nullable=False)
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


def start_mappers():
    mapper(order_entity.OrderItem, OrderItem)
    mapper(chat_session_entity.ChatSession, ChatSession)
    mapper(website_entity.WebsiteSession, WebsiteSession)
