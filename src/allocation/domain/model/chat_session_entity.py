from abc import ABC

from allocation.domain.model.root_entity import Entity
from datetime import datetime


class ChatSession(Entity):
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
        return object.__repr__(self)

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

    def is_refunded(self) -> bool:
        raise NotImplementedError
