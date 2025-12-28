# import pytest
# from sqlalchemy.orm import Session
# from fastapi import HTTPException

# from app.services.status_service import StatusService
# from app.schemas.common import ApplicationStatus
# from app.db.models.job_application import JobApplication
# from app.db.models.status_history import StatusHistory

# def create_application(session: Session, status: ApplicationStatus):
#     app = JobApplication(
#         user_id=1,
#         company_id=1,
#         role_title="Backend Engineer",
#         source="portal",
#         current_status=status.value,
#     )
#     session.add(app)
#     session.commit()
#     session.refresh(app)
#     return app

# #1

# def test_valid_status_transition(session: Session):
#     app = create_application(session, ApplicationStatus.APPLIED)

#     service = StatusService(session)
#     service.change_status(
#     application_id=app.application_id,
#     user_id=app.user_id,
#     new_status=ApplicationStatus.APPLIED,
# )


#     updated = session.get(JobApplication, app.application_id)
#     assert updated.current_status == ApplicationStatus.INTERVIEW.value

# #2

# def test_status_history_created(session: Session):
#     app = create_application(session, ApplicationStatus.APPLIED)

#     service = StatusService(session)
#     service.change_status(
#         application_id=app.application_id,
#         new_status=ApplicationStatus.OA,
#     )

#     history = (
#         session.query(StatusHistory)
#         .filter_by(application_id=app.application_id)
#         .all()
#     )

#     assert len(history) == 1
#     assert history[0].status == ApplicationStatus.OA.value

# #3


# def test_invalid_status_transition(session: Session):
#     app = create_application(session, ApplicationStatus.REJECTED)

#     service = StatusService(session)

#     with pytest.raises(HTTPException) as exc:
#         service.change_status(
#             application_id=app.application_id,
#             new_status=ApplicationStatus.INTERVIEW,
#         )

#     assert exc.value.status_code == 400

# #4

# def test_application_not_found(session: Session):
#     service = StatusService(session)

#     with pytest.raises(HTTPException) as exc:
#         service.change_status(
#             application_id=9999,
#             new_status=ApplicationStatus.APPLIED,
#         )

#     assert exc.value.status_code == 404

import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.status_service import StatusService
from app.schemas.common import ApplicationStatus
from app.db.models.job_application import JobApplication
from app.db.models.status_history import StatusHistory


def create_application(session: Session, status: ApplicationStatus):
    app = JobApplication(
        user_id=1,
        company_id=1,
        role_title="Backend Engineer",
        source="portal",
        current_status=status.value,
    )
    session.add(app)
    session.commit()
    session.refresh(app)
    return app


# 1️⃣ valid transition
def test_valid_status_transition(session: Session):
    app = create_application(session, ApplicationStatus.APPLIED)

    service = StatusService(session)
    service.change_status(
        application_id=app.application_id,
        user_id=app.user_id,
        new_status=ApplicationStatus.INTERVIEW,
    )

    updated = session.get(JobApplication, app.application_id)
    assert updated.current_status == ApplicationStatus.INTERVIEW.value


# 2️⃣ status history written
def test_status_history_created(session: Session):
    app = create_application(session, ApplicationStatus.APPLIED)

    service = StatusService(session)
    service.change_status(
        application_id=app.application_id,
        user_id=app.user_id,
        new_status=ApplicationStatus.OA,
    )

    history = (
        session.query(StatusHistory)
        .filter(StatusHistory.application_id == app.application_id)
        .all()
    )

    assert len(history) == 1
    assert history[0].status == ApplicationStatus.OA.value


# 3️⃣ invalid transition
def test_invalid_status_transition(session: Session):
    app = create_application(session, ApplicationStatus.REJECTED)

    service = StatusService(session)

    with pytest.raises(HTTPException) as exc:
        service.change_status(
            application_id=app.application_id,
            user_id=app.user_id,
            new_status=ApplicationStatus.INTERVIEW,
        )

    assert exc.value.status_code == 400


# 4️⃣ application not found
def test_application_not_found(session: Session):
    service = StatusService(session)

    with pytest.raises(HTTPException) as exc:
        service.change_status(
            application_id=9999,
            user_id=1,
            new_status=ApplicationStatus.APPLIED,
        )

    assert exc.value.status_code == 404
