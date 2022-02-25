import abc


class Entity(abc.ABC):
    def __enter__(self):
        return self

    @abc.abstractmethod
    def add(self, session, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, session, entity, entity_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, session, entity, entity_id):
        raise NotImplementedError
