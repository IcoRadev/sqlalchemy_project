import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from testsuite import test_utils
from src.allocation import config
from src.allocation.adapters.orm import metadata, start_mappers


@pytest.fixture
def session(session_factory):
    return session_factory()


@pytest.fixture(scope="session")
def mysql_db():
    engine = create_engine(config.get_configuration()["url_tests"])
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def fake_uow():
    return test_utils.FakeUnitOfWork()


@pytest.fixture
def mysql_start(mysql_db):
    start_mappers()
    yield sessionmaker(bind=mysql_db)()
    clear_mappers()
