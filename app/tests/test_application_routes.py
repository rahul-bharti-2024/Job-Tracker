import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.db.models.base import Base
from app.db.session import get_session

load_dotenv()

# ---------- DB SETUP ----------
TEST_DB_URL = os.getenv("TEST_POSTGRES_URL")

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# IMPORTANT: import models so metadata is populated
from app.db.models import *  # noqa


def setup_module(module):
    """Run once for this test file."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


# ---------- DEPENDENCY OVERRIDE ----------
def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


# ---------- APP + CLIENT ----------
from app.main import app  # import AFTER overrides exist

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


# ---------- HELPERS ----------
def create_application(company_id=7, role_title="Backend Engineer"):
    payload = {
        "company_id": company_id,
        "role_title": role_title,
        "source": "portal",
    }
    res = client.post("/applications", json=payload)
    assert res.status_code == 200
    return res.json()["application_id"]


# ---------- TESTS ----------
def test_list_applications():
    res = client.get("/applications")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_change_status():
    app_id = create_application(company_id=1, role_title="ML Engineer")

    res = client.post(
        f"/applications/{app_id}/status",
        json={"new_status": "APPLIED"},
    )
    assert res.status_code == 200

    # verify via read endpoint
    res = client.get("/applications")
    apps = {a["application_id"]: a for a in res.json()}

    assert apps[app_id]["current_status"] == "APPLIED"


def test_filter_by_status():
    a1 = create_application(company_id=1, role_title="BE")
    a2 = create_application(company_id=2, role_title="ML")

    client.post(f"/applications/{a2}/status", json={"new_status": "APPLIED"})

    res = client.get("/applications?status=APPLIED")
    assert res.status_code == 200

    ids = {a["application_id"] for a in res.json()}
    assert a2 in ids
    assert a1 not in ids


def test_filter_by_tag():
    a = create_application(company_id=3, role_title="DS")

    res = client.post(
        f"/applications/{a}/tags",
        json={"name": "referral"},
    )
    assert res.status_code == 200

    res = client.get("/applications?tag=referral")
    assert res.status_code == 200

    ids = {x["application_id"] for x in res.json()}
    assert a in ids
