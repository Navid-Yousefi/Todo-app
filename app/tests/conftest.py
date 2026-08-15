from main import app
from fastapi.testclient import TestClient
from core.database import Base, create_engine, sessionmaker, get_db
from sqlalchemy import StaticPool
import pytest
from faker import Faker
from users.model import UserModel
from tasks.models import TaskModel

faker = Faker()


SQLALCHEMY_DATABASE_URL = 'sqlite:///memory'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope='package')
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
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope='session', autouse=True)
def rearup_and_down_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def anon_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='package', autouse=True)
def generate_mock_data(db_session):

    # create a user
    user = UserModel(username='navid', email='navid@gmail.com',is_active=True)
    user.set_password('12345678')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # create tasks
    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            TaskModel(
                title=faker.sentence(nb_words=6),
                description=faker.text(),
                is_completed=faker.boolean()
            )
        )
    db_session.add_all(tasks_list)
    db_session.commit()
    
