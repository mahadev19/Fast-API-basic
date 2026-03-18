import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db

# -------------------------------
# USE SQLITE FOR TESTING
# — no PostgreSQL needed in CI
# -------------------------------
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in test DB
Base.metadata.create_all(bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# -------------------------------
# TESTS
# -------------------------------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Patient Management System API"}

def test_about():
    response = client.get("/about")
    assert response.status_code == 200

def test_create_patient():
    response = client.post("/create", json={
        "id": "P001",
        "name": "Test User",
        "city": "Pune",
        "age": 25,
        "gender": "male",
        "height": 1.75,
        "weight": 70
    })
    assert response.status_code == 201

def test_view_patients():
    response = client.get("/view")
    assert response.status_code == 200

def test_invalid_login():
    response = client.post("/login", data={
        "username": "wrong",
        "password": "wrong"
    })
    assert response.status_code == 400