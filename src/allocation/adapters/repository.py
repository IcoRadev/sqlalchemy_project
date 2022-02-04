import abc
from allocation.domain.model.root_entity import Entity


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, entity: object, entity_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, entity: object, entity_id: int):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)

    def remove(self, entity, entity_id):
        entity = self.session.query(entity).filter(entity.id == entity_id).first()
        self.session.delete(entity)

    def get(self, entity: object, entity_id):
        entity = self.session.query(entity).filter(entity.id == entity_id).first()
        return entity

    def list(self):
        return self.session.query(Entity).all()
