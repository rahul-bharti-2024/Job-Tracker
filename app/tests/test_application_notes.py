# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# from app.db.models.base import Base
# from app.db.session import get_session
# from app.api.dependencies.auth import get_current_user_id
# from app.main import app
# TEST_DB_URL = os.getenv("TEST_POSTGRES_URL")

# engine = create_engine(TEST_DB_URL)
# TestingSessionLocal = sessionmaker(bind=engine)

# # import all models so tables exist
# from app.db.models import *  # noqa

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


# def override_get_session():
#     db = TestingSessionLocal()
#     try:
#         yield db
#         db.commit()
#     finally:
#         db.close()


# def override_get_current_user_id():
#     return 1


# app.dependency_overrides[get_session] = override_get_session
# app.dependency_overrides[get_current_user_id] = override_get_current_user_id

# client = TestClient(app)
# def create_application(company_id=1, role_title="Backend Engineer"):
#     payload = {
#         "company_id": company_id,
#         "role_title": role_title,
#         "source": "portal",
#     }
#     res = client.post("/applications", json=payload)
#     assert res.status_code == 200
#     return res.json()["application_id"]

# def test_create_note_for_application():
#     app_id = create_application()

#     payload = {
#         "application_id": app_id,
#         "content": "HR called for initial screening",
#     }

#     res = client.post("/notes", json=payload)
#     assert res.status_code == 200

#     data = res.json()
#     assert data["content"] == "HR called for initial screening"
#     assert data["application_id"] == app_id

# def test_list_application_notes():
#     app_id = create_application(company_id=2, role_title="ML Engineer")

#     client.post(
#         "/notes",
#         json={
#             "application_id": app_id,
#             "content": "Sent resume via referral",
#         },
#     )

#     client.post(
#         "/notes",
#         json={
#             "application_id": app_id,
#             "content": "Recruiter replied",
#         },
#     )

#     res = client.get(f"/applications/{app_id}/notes")
#     assert res.status_code == 200

#     notes = res.json()
#     assert len(notes) == 2
#     assert notes[0]["content"] in {
#         "Recruiter replied",
#         "Sent resume via referral",
#     }
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models.base import Base
from app.db.session import get_session
from app.api.dependencies.auth import get_current_user_id
from app.main import app

# IMPORTANT: import models so metadata is populated
from app.db.models import *  # noqa


TEST_DB_URL = os.getenv("TEST_POSTGRES_URL")

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def setup_module(module):
    """Runs once for this test file."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def override_get_current_user_id():
    return 1


app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_current_user_id] = override_get_current_user_id

client = TestClient(app)


def create_application(company_id=1, role_title="Backend Engineer"):
    payload = {
        "company_id": company_id,
        "role_title": role_title,
        "source": "portal",
    }
    res = client.post("/applications", json=payload)
    assert res.status_code == 200
    return res.json()["application_id"]


def test_create_note_for_application():
    app_id = create_application()

    payload = {
        "application_id": app_id,
        "content": "HR called for initial screening",
    }

    res = client.post("/notes", json=payload)
    assert res.status_code == 200

    data = res.json()
    assert data["content"] == "HR called for initial screening"
    assert data["application_id"] == app_id


def test_list_application_notes():
    app_id = create_application(company_id=2, role_title="ML Engineer")

    client.post(
        "/notes",
        json={"application_id": app_id, "content": "Sent resume via referral"},
    )

    client.post(
        "/notes",
        json={"application_id": app_id, "content": "Recruiter replied"},
    )

    res = client.get(f"/applications/{app_id}/notes")
    assert res.status_code == 200

    notes = res.json()
    assert len(notes) == 2

    contents = {note["content"] for note in notes}
    assert contents == {
        "Sent resume via referral",
        "Recruiter replied",
    }
