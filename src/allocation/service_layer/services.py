from __future__ import annotations
from typing import Optional
from datetime import datetime

from allocation.domain.model.root_entity import Entity
from allocation.service_layer import unit_of_work


def add_entity(uow: unit_of_work.AbstractUnitOfWork, entity: Entity):
    with uow:
        uow.entity.add(entity)
        uow.commit()


def remove_entity(uow: unit_of_work.AbstractUnitOfWork, entity: object, entity_id):
    with uow:
        uow.entity.remove(entity, entity_id)
        uow.commit()


def get_entity(uow: unit_of_work.AbstractUnitOfWork, entity: object, entity_id: int):
    with uow:
        entity = uow.entity.get(entity, entity_id)
        yield entity
