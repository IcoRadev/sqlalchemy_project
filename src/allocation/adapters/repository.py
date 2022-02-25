import abc
from allocation.domain.batch_entity import Batch


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, batch: Batch, batch_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, batch: Batch, batch_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, batch: Batch):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        batch.add(self.session, batch)

    def remove(self, batch: Batch, batch_id: int):
        batch.remove(self.session, batch, batch_id)

    def get(self, batch: Batch, batch_id: int):
        batch.get(self.session, batch, batch_id)
        return batch

    def list(self, batch: Batch):
        return self.session.query(batch).all()

