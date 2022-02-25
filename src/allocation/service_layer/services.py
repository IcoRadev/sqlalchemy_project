from __future__ import annotations
from typing import Optional
from datetime import datetime

from allocation.domain.batch_entity import Batch
from allocation.service_layer import unit_of_work


def add_batch(uow: unit_of_work.AbstractUnitOfWork, batch):  # , entity_list: list, entity_type: object):
    with uow:
        uow.batch.add(batch)
        # allocate(uow, entity_type, entity_list, batch.tag)
        uow.commit()


def remove_batch(uow: unit_of_work.AbstractUnitOfWork, batch, batch_id):
    with uow:
        uow.batch.remove(batch, batch_id)
        uow.commit()


def get_batch(uow: unit_of_work.AbstractUnitOfWork, batch, batch_id: int):
    with uow:
        result = uow.batch.get(batch, batch_id)
        return result


def allocate(uow: unit_of_work.AbstractUnitOfWork, entity_type, entity_list: list, batch_tag: str):
    for item in entity_list:
        constructed_entity = entity_type(*list(item.values()))
        uow.batch.add(constructed_entity)

    uow.commit()
