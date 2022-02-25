from abc import ABC

from allocation.domain.model.root_entity import Entity
from datetime import datetime


class ChatSession(Entity):
    user_id = None
    representative_id = None
    website_session_id = None
    start_time = None
    end_time = None

    def __init__(self, representative_id: int,
                 user_id: int,
                 website_session_id: int,
                 start_time: datetime,
                 end_time: datetime):

        self.user_id = user_id
        self.representative_id = representative_id
        self.website_session_id = website_session_id
        self.start_time = start_time
        self.end_time = end_time

    def __enter__(self):
        super().__init__()

    def __repr__(self) -> str:
        # return object.__repr__(self)
        return "Chat_at: {}, user: {}, representative: {}".format(self.start_time, self.user_id, self.representative_id)

    def __eq__(self, entity) -> bool:
        self_items = self.__dict__.items().__iter__()
        entity_items = self.__dict__.items().__iter__()
        try:
            while self_items:
                if not next(self_items) == next(entity_items):
                    return False
        except StopIteration:
            pass
        return True

    @classmethod
    def add(cls, session, entity: Entity):
        session.add(entity)

    @classmethod
    def remove(cls, session, entity: Entity, entity_id):
        entity = session.query(entity).filter(entity.website_session_id == entity_id).first()
        session.delete(entity)

    @classmethod
    def get(cls, session, entity: Entity, entity_id):
        entity = session.query(entity).filter(entity.website_session_id == entity_id).first()
        return entity.__repr__()

    @classmethod
    def list(cls, session):
        return session.query(cls).all()


class ChatAllocation:
    def __init__(self, batch_tag: str, ref_id: int):
        self.batch_tag = batch_tag
        self.ref_id = ref_id

    def __enter__(self):
        super().__init__()

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
