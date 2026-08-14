from main import app
from fastapi.testclient import TestClient
from core.database import Base, create_engine, sessionmaker, get_db
from sqlalchemy import StaticPool
import pytest


SQLALCHEMY_DATABASE_URL = 'sqlite:///memory'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope='module')
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module', autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db,None)


@pytest.fixture(scope='session', autouse=True)
def rearup_and_down_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def anon_client():
    client = TestClient(app)
    yield client
