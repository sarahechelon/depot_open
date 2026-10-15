import pathlib
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import get_session
from app.main import app
from app.models import Base


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def db_session(tmp_path: pathlib.Path) -> Iterator[Session]:
    """Isolated SQLite file per test; parallel-safe under xdist."""
    engine = create_engine(
        f"sqlite:///{tmp_path}/test.db", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def api_client(db_session: Session) -> Iterator[TestClient]:
    """Client whose /products endpoints hit the isolated test database."""

    def override() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_session] = override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
