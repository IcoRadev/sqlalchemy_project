from src.allocation.service_layer import services
from src.allocation.domain.model.chat_session_entity import ChatSession


def test_add_chat_session(fake_uow):
    item_under_test = ChatSession(1, 178784, 206362, "2014-03-01 00:18:13", "2014-03-01 02:18:13")

    services.add_batch(fake_uow, item_under_test)
    assert fake_uow.batch.get(item_under_test, 206362) is not None


def test_remove_chat_session(fake_uow):
    item_under_test = ChatSession(1, 178784, 206362, "2014-03-01 00:18:13", "2014-03-01 02:18:13")

    services.add_batch(fake_uow, item_under_test)
    services.remove_batch(fake_uow, item_under_test, 206362)

    assert fake_uow.batch.get(item_under_test, 206362) is None
