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

# # IMPORTANT: import models so tables exist
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

# def create_application(comapny_id=1, role_title="Backend Engineer"):
#     payload = {
#         "company_id": comapny_id,
#         "role_title": role_title,
#         "source": "portal",
#     }
#     res = client.post("/applications", json=payload)
#     assert res.status_code == 200
#     return res.json()["application_id"]


# def test_attach_tag():
#     app_id = create_application()

#     res = client.post(
#         f"/applications/{app_id}/tags",
#         json={"name": "referral"},
#     )

#     assert res.status_code == 200


# def test_list_tags():
#     app_id = create_application(comapny_id=2, role_title="ML Engineer")

#     client.post(
#         f"/applications/{app_id}/tags",
#         json={"name": "referral"},
#     )

#     res = client.get(f"/applications/{app_id}/tags")
#     assert res.status_code == 200

#     tags = res.json()
#     assert len(tags) == 1
#     assert tags[0]["name"] == "referral"


# def test_detach_tag():
#     app_id = create_application(comapny_id=3, role_title="Data Scientist")

#     client.post(
#         f"/applications/{app_id}/tags",
#         json={"name": "referral"},
#     )

#     tags = client.get(f"/applications/{app_id}/tags").json()
#     tag_id = tags[0]["tag_id"]

#     res = client.delete(f"/applications/{app_id}/tags/{tag_id}")
#     assert res.status_code == 200

#     tags = client.get(f"/applications/{app_id}/tags").json()
#     assert tags == []
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models.base import Base
from app.db.session import get_session
from app.api.dependencies.auth import get_current_user_id

# IMPORTANT: import models so tables exist
from app.db.models import *  # noqa


TEST_DB_URL = os.getenv("TEST_POSTGRES_URL")

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def setup_module(module):
    """Run once for this test file."""
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


from app.main import app  # import AFTER overrides are defined

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


def test_attach_tag():
    app_id = create_application()

    res = client.post(
        f"/applications/{app_id}/tags",
        json={"name": "referral"},
    )
    assert res.status_code == 200

    # verify tag exists via GET
    res = client.get(f"/applications/{app_id}/tags")
    assert res.status_code == 200

    tags = res.json()
    assert len(tags) == 1
    assert tags[0]["name"] == "referral"


def test_list_tags():
    app_id = create_application(company_id=2, role_title="ML Engineer")

    client.post(
        f"/applications/{app_id}/tags",
        json={"name": "referral"},
    )

    res = client.get(f"/applications/{app_id}/tags")
    assert res.status_code == 200

    tags = res.json()
    assert len(tags) == 1
    assert tags[0]["name"] == "referral"


def test_detach_tag():
    app_id = create_application(company_id=3, role_title="Data Scientist")

    client.post(
        f"/applications/{app_id}/tags",
        json={"name": "referral"},
    )

    tags = client.get(f"/applications/{app_id}/tags").json()
    assert len(tags) == 1

    tag_id = tags[0]["tag_id"]

    res = client.delete(f"/applications/{app_id}/tags/{tag_id}")
    assert res.status_code == 200

    res = client.get(f"/applications/{app_id}/tags")
    assert res.status_code == 200
    assert res.json() == []
