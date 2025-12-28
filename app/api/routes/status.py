# # app/api/routes/status.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.schemas.status import StatusChangeRequest
# from app.services.status_service import StatusService
# from app.db.session import get_session

# router = APIRouter(prefix="/applications")

# @router.post("/{application_id}/status")
# def change_status(
#     application_id: int,
#     payload: StatusChangeRequest,
#     session: Session = Depends(get_session),
# ):
#     service = StatusService(session)
#     service.change_status(
#         application_id=application_id,
#         new_status=payload.new_status,
#     )
#     return {"status": "ok"}
# app/api/routes/status.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.status import StatusChangeRequest
from app.services.status_service import StatusService
from app.db.session import get_session
from app.api.dependencies.auth import get_current_user_id

router = APIRouter(
    prefix="/applications",
    tags=["status"],
)

@router.post(
    "/{application_id}/status",
    summary="Change application status",
    description=(
        "Update the status of a job application owned by the authenticated user. "
        "Status transitions are validated against allowed state changes."
    ),
)
def change_status(
    application_id: int,
    payload: StatusChangeRequest,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = StatusService(session)
    service.change_status(
        application_id=application_id,
        new_status=payload.new_status,
        user_id=user_id,
    )
    return {"status": "ok"}
