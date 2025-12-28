# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.db.session import get_session
# from app.services.note_service import NoteService
# from app.api.dependencies.auth import get_current_user_id
# from app.schemas.note import NoteCreate
# from app.schemas.note import NoteResponse

# router = APIRouter(tags=["notes"])

# @router.post("/notes")
# def add_note(
#     payload: NoteCreate,  # { "application_id": 1, "content": "HR called" }
#     session: Session = Depends(get_session),
#     user_id: int = Depends(get_current_user_id),
# ):
#     service = NoteService(session)
#     return service.add_note_to_application(
#         user_id=user_id,
#         application_id=payload["application_id"],
#         content=payload["content"],
#     )


# @router.get("/applications/{application_id}/notes",response_model=list[NoteResponse])

# def list_notes(
#     application_id: int,
#     session: Session = Depends(get_session),
#     user_id: int = Depends(get_current_user_id),
# ):
#     service = NoteService(session)
#     return service.list_application_notes(
#         user_id=user_id,
#         application_id=application_id,
#     )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.note_service import NoteService
from app.api.dependencies.auth import get_current_user_id
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter(tags=["notes"])

@router.post(
    "/notes",
    response_model=NoteResponse,
    summary="Add a note to an application",
    description="Add a note to a job application owned by the authenticated user.",
)
def add_note(
    payload: NoteCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = NoteService(session)
    return service.add_note_to_application(
        user_id=user_id,
        application_id=payload.application_id,
        content=payload.content,
    )

@router.get(
    "/applications/{application_id}/notes",
    response_model=list[NoteResponse],
    summary="List notes for an application",
    description="Retrieve all notes for a job application owned by the authenticated user.",
)
def list_notes(
    application_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = NoteService(session)
    return service.list_application_notes(
        user_id=user_id,
        application_id=application_id,
    )
