# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.db.session import get_session
# from app.services.application_service import ApplicationService
# from app.services.application_read_service import ApplicationReadService
# from app.services.status_service import StatusService
# from app.schemas.application import ApplicationCreate, ApplicationResponse
# from app.schemas.status import StatusChangeRequest
# from app.api.dependencies.auth import get_current_user_id
# from typing import Optional

# router = APIRouter(prefix="/applications", tags=["applications"])

# @router.post("/",response_model=ApplicationResponse)
# def create_application(
#         payload: ApplicationCreate,
#         session: Session = Depends(get_session),
#         user_id: int = Depends(get_current_user_id),  # Assuming a function to get current user ID
# ):
#     service = ApplicationService(session)
#     app = service.create_application(user_id=user_id, data=payload)  
#     return app

# #for understanding , payload should be ApplicationCreate model ,  session  gets session from session factory 

# # session: Session = Depends(get_session)
# # Dependency injection
# # FastAPI:
# # Calls get_session()
# # Injects a DB session
# # Cleans it up after request

# # service is instance of ApplicationService with session passed
# # create_application method of service is called with user_id and payload data to create a new application
# # FastAPI: return app

# # Converts it to ApplicationResponse
# # Serializes to JSON
# # Sends HTTP response
# @router.get("/", response_model=list[ApplicationResponse])
# @router.get("/", response_model=list[ApplicationResponse])
# def list_applications(
#     status: Optional[str] = None,
#     tag: Optional[str] = None,
#     session: Session = Depends(get_session),
#     user_id: int = Depends(get_current_user_id),
# ):
#     service = ApplicationReadService(session)
#     return service.list_applications_filtered(
#         user_id=user_id,
#         status=status,
#         tag=tag,
#     )
    

# @router.get("/{application_id}", response_model=ApplicationResponse)
# def get_application(
#     application_id: int,
#     session: Session = Depends(get_session),
# ):
#     service = ApplicationReadService(session)
#     return service.get_application(application_id)


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
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_session
from app.services.application_service import ApplicationService
from app.services.application_read_service import ApplicationReadService
from app.services.status_service import StatusService
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.schemas.status import StatusChangeRequest
from app.api.dependencies.auth import get_current_user_id

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post(
    "/",
    response_model=ApplicationResponse,
    summary="Create a job application",
    description="Create a new job application for the authenticated user.",
)
def create_application(
    payload: ApplicationCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = ApplicationService(session)
    return service.create_application(user_id=user_id, data=payload)

@router.get(
    "/",
    response_model=list[ApplicationResponse],
    summary="List job applications",
    description="List all job applications for the authenticated user, with optional filtering by status or tag.",
)
def list_applications(
    status: Optional[str] = None,
    tag: Optional[str] = None,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = ApplicationReadService(session)
    return service.list_applications_filtered(
        user_id=user_id,
        status=status,
        tag=tag,
    )

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Get a job application",
    description="Retrieve a single job application owned by the authenticated user.",
)
def get_application(
    application_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = ApplicationReadService(session)
    return service.get_application(application_id, user_id=user_id)

@router.post(
    "/{application_id}/status",
    summary="Change application status",
    description="Update the status of a job application owned by the authenticated user.",
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

