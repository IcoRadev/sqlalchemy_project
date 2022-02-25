from allocation.domain.model.root_entity import Entity


class Batch(Entity):
    def __init__(self, ref_type: object, tag: str):
        self.ref_type = ref_type
        self.tag = tag
        self.chat_allocations = set()

    def __eq__(self, other_batch):
        return self == other_batch

    def __repr__(self) -> str:
        return "Batch: {}, Entity Types {}".format(self.tag, self.ref_type)

    def __enter__(self):
        super().__init__()

    @classmethod
    def add(cls, session, entity: Entity):
        session.add(entity)

    @classmethod
    def remove(cls, session, entity: Entity, entity_id):
        entity = session.query(entity).filter(entity.id == entity_id).first()
        import pdb;pdb.set_trace()
        session.delete(entity)

    @classmethod
    def get(cls, session, entity: Entity, entity_id):
        entity = session.query(entity).filter(entity.id == entity_id).first()
        return entity.__repr__()

    @classmethod
    def list(cls, session, entity: Entity):
        return session.query(entity).all()
    #
    # @classmethod
    # def get_by_tag(cls, session, tag: str):
    #     entity = session.query(cls).filter(cls.tag == tag).first()
    #     return entity.__repr__()
    #
    # def allocate(self, session, entity: Entity):
    #     pass



