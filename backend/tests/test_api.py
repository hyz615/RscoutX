import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.db.session import get_session
from app.models.models import Team, Robot, Driver


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_team(client: TestClient):
    """Test creating a team"""
    response = client.post(
        "/api/teams/",
        json={
            "team_number": "1234A",
            "team_name": "Test Team",
            "organization": "Test Org",
            "region": "Test Region"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["team_number"] == "1234A"
    assert data["team_name"] == "Test Team"
    assert "id" in data


def test_get_teams(client: TestClient):
    """Test getting all teams"""
    # Create a team first
    client.post(
        "/api/teams/",
        json={
            "team_number": "1234A",
            "team_name": "Test Team",
            "organization": "Test Org",
            "region": "Test Region"
        }
    )
    
    response = client.get("/api/teams/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["team_number"] == "1234A"


def test_path_render(client: TestClient):
    """Test path rendering"""
    response = client.post(
        "/api/path/render",
        json={
            "method": "polyline",
            "points": [
                {"x": 100, "y": 100},
                {"x": 200, "y": 200},
                {"x": 300, "y": 150}
            ],
            "style": {
                "color": "#FF0000",
                "width": 3
            },
            "coordinate_system": "pixel",
            "return_image": True,
            "return_overlay": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "image_base64" in data


def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
