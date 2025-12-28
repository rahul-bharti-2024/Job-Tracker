# from sqlalchemy.orm import Session

# from app.services.application_service import ApplicationService
# from app.schemas.application import ApplicationCreate
# from app.schemas.common import ApplicationStatus
# from app.db.models.job_application import JobApplication
# from app.db.models.status_history import StatusHistory

# def make_payload():
#     return ApplicationCreate(
#         company_id=1,
#         role_title="Backend Engineer",
#         source="portal",
#     )

# def test_create_application_sets_saved_status(session: Session):
#     service = ApplicationService(session)

#     app = service.create_application(
#         user_id=1,
#         data=make_payload(),
#     )

#     db_app = session.get(JobApplication, app.application_id)

#     assert db_app is not None
#     assert db_app.current_status == ApplicationStatus.SAVED.value

# def test_create_application_writes_status_history(session: Session):
#     service = ApplicationService(session)

#     app = service.create_application(
#         user_id=1,
#         data=make_payload(),
#     )

#     history = (
#         session.query(StatusHistory)
#         .filter_by(application_id=app.application_id)
#         .all()
#     )

#     assert len(history) == 1
#     assert history[0].status == ApplicationStatus.SAVED.value

from sqlalchemy.orm import Session

from app.services.application_service import ApplicationService
from app.schemas.application import ApplicationCreate
from app.schemas.common import ApplicationStatus
from app.db.models.job_application import JobApplication
from app.db.models.status_history import StatusHistory


def make_payload():
    return ApplicationCreate(
        company_id=1,
        role_title="Backend Engineer",
        source="portal",
    )


def test_create_application_sets_saved_status(session: Session):
    service = ApplicationService(session)

    app = service.create_application(
        user_id=1,
        data=make_payload(),
    )

    db_app = session.get(JobApplication, app.application_id)

    assert db_app is not None
    assert db_app.user_id == 1
    assert db_app.current_status == ApplicationStatus.SAVED.value


def test_create_application_writes_status_history(session: Session):
    service = ApplicationService(session)

    app = service.create_application(
        user_id=1,
        data=make_payload(),
    )

    history = (
        session.query(StatusHistory)
        .filter(StatusHistory.application_id == app.application_id)
        .all()
    )

    assert len(history) == 1
    assert history[0].status == ApplicationStatus.SAVED.value
