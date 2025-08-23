import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from ..models import Base, Todos, User
from ..main import app
from ..routers.auth import bcrypt_context

# In-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



# Override authentication to always return a fake user
def override_get_current_user():
    return {"user_id": 1, "username": "testuser", "user_role": "admin"}


client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    todo = Todos(
        title="Learn to code!",
        description="whatever",
        priority=5,
        complete=False,
        owner_id=1
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    db.execute(text("DELETE FROM todos"))
    db.commit()
    db.close()

@pytest.fixture
def test_user():
    user = User(
        username = 'user',
        email = 'user@example.com',
        first_name = 'user',
        last_name = 'bot',
        hashed_password = bcrypt_context.hash('testpassword'),
        role = 'admin',
        phone_number = '0215673546'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    db.execute(text('DELETE FROM users'))
    db.commit()
    db.close()