from src.allocation.adapters import repository
from src.allocation.service_layer import services, unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self):
        self.entity = None

    def add(self, entity):
        self.entity = entity

    def get(self, entity, entity_id):
        try:
            return self.entity.website_session_id == entity_id
        except AttributeError:
            return None

    def remove(self, entity, batch_id: int):
        self.entity = None

    def list(self, entity):
        return entity.__repr__()


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batch = FakeRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
