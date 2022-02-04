from allocation.domain.model.root_entity import Entity


class Batch:
    def __init__(self, entity: Entity):
        self.allocations = set()

    def __eq__(self, other_batch):
        return self == other_batch

    def allocate(self, entity: Entity, action: str):
        self.allocations.add({entity: action})

    def deallocate(self, entity: Entity):
        self.allocations.remove(entity)

    def make_transaction(self):
        raise NotImplementedError
        for pair in self.allocations:
            pass
