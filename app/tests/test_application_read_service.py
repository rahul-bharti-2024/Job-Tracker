import pytest
from fastapi import HTTPException
from app.services.application_read_service import ApplicationReadService
from app.db.models.job_application import JobApplication
from app.schemas.common import ApplicationStatus


def seed_app(
    session,
    *,
    user_id=1,
    company_id=1,
    role_title="Backend Engineer",
):
    app = JobApplication(
        user_id=user_id,
        company_id=company_id,
        role_title=role_title,
        source="portal",
        current_status=ApplicationStatus.SAVED.value,
    )
    session.add(app)
    session.commit()
    session.refresh(app)
    return app


def test_get_application_success(session):
    app = seed_app(session)

    service = ApplicationReadService(session)
    found = service.get_application(
        application_id=app.application_id,
        user_id=app.user_id,
    )

    assert found is not None
    assert found.application_id == app.application_id
    assert found.user_id == app.user_id


def test_get_application_wrong_user_raises_404(session):
    app = seed_app(session, user_id=1)

    service = ApplicationReadService(session)

    with pytest.raises(HTTPException) as exc:
        service.get_application(
            application_id=app.application_id,
            user_id=999,
        )

    assert exc.value.status_code == 404


def test_list_applications_by_user(session):
    seed_app(session, user_id=1, company_id=1, role_title="Backend Engineer")
    seed_app(session, user_id=1, company_id=2, role_title="ML Engineer")
    seed_app(session, user_id=2, company_id=3, role_title="Backend Engineer")

    service = ApplicationReadService(session)
    apps = service.list_applications(user_id=1)

    assert len(apps) == 2
    assert {app.user_id for app in apps} == {1}
