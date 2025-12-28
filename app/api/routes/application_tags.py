# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.schemas.tag import TagCreate
# from app.db.session import get_session
# from app.services.tag_service import TagService
# from app.api.dependencies.auth import get_current_user_id
# from app.schemas.tag import TagResponse
# router = APIRouter(
#     prefix="/applications/{application_id}/tags",
#     tags=["tags"],
# )
# @router.post("/")
# def attach_tag(
#     application_id: int,
#     payload: TagCreate,  # { "name": "referral" }
#     session: Session = Depends(get_session),
#     user_id: int = Depends(get_current_user_id),
# ):
#     service = TagService(session)
#     service.attach_tag(
#         application_id=application_id,
#         user_id=user_id,
#         tag_name=payload["name"],
#     )
#     return {"status": "ok"}

# @router.delete("/{tag_id}")
# def detach_tag(
#     application_id: int,
#     tag_id: int,
#     session: Session = Depends(get_session),
#     user_id: int = Depends(get_current_user_id),
# ):
#     service = TagService(session)
#     service.detach_tag(
#         application_id=application_id,
#         user_id=user_id,
#         tag_id=tag_id,
#     )
#     return {"status": "ok"}

# @router.get("/", response_model=list[TagResponse])
# def list_tags(
#     application_id: int,
#     session: Session = Depends(get_session),
#     user_id: int = Depends(get_current_user_id),
# ):
#     service = TagService(session)
#     return service.list_tags(
#         application_id=application_id,
#         user_id=user_id,
#     )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.tag import TagCreate, TagResponse
from app.db.session import get_session
from app.services.tag_service import TagService
from app.api.dependencies.auth import get_current_user_id

router = APIRouter(
    prefix="/applications/{application_id}/tags",
    tags=["tags"],
)

@router.post(
    "/",
    summary="Attach a tag to an application",
    description="Attach a tag (creates it if it does not exist) to a job application owned by the current user.",
)
def attach_tag(
    application_id: int,
    payload: TagCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TagService(session)
    service.attach_tag(
        application_id=application_id,
        user_id=user_id,
        tag_name=payload.name,
    )
    return {"status": "ok"}

@router.delete(
    "/{tag_id}",
    summary="Detach a tag from an application",
    description="Remove a tag from a job application owned by the current user.",
)
def detach_tag(
    application_id: int,
    tag_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TagService(session)
    service.detach_tag(
        application_id=application_id,
        user_id=user_id,
        tag_id=tag_id,
    )
    return {"status": "ok"}

@router.get(
    "/",
    response_model=list[TagResponse],
    summary="List tags for an application",
    description="Retrieve all tags attached to a job application owned by the current user.",
)
def list_tags(
    application_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TagService(session)
    return service.list_tags(
        application_id=application_id,
        user_id=user_id,
    )
