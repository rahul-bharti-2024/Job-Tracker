# from fastapi import APIRouter,Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.db.session import get_session
# from app.services.JobApplicationService import JobApplicationService
# from app.api.schemas.job_applications import(
#     CreateApplicationRequest, UpdateApplicationRequest
# )
# from app.api.dependencies.auth import get_current_user
# from app.db.models.user import User



# router= APIRouter(prefix="/applications", tags=["job_applications"])


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_application(
#     request: CreateApplicationRequest,
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     service= JobApplicationService(session)
#     try:
#         application= service.create_application(
#             user_id= user.user_id,
#             **request.model_dump(),
#         )
#         return application
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
    

# @router.get("/")
# def list_applications(
    
#     status: str | None = None,
#     company_id: int | None = None,
#     limit: int = 20,
#     offset: int = 0,
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
    
# ):
    
#     service = JobApplicationService(session)
    
#     result = service.list_applications(
#         user_id=user.user_id,
#         status=status,
#         company_id=company_id,
#         limit=limit,
#         offset=offset,
#     )
#     return result


# @router.get("/{application_id}")
# def get_application(
    
#     application_id:int,
#     session : Session= Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     service= JobApplicationService(session)
#     try:
#         application= service.get_application(
#             user_id= user.user_id,
#             application_id= application_id,
#         )
#         return application
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e)) 
    
# @router.patch("/{application_id}/status", status_code=status.HTTP_204_NO_CONTENT)
# def update_application_status(
#     application_id: int,
#     request: UpdateApplicationRequest,
#     session: Session = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     service = JobApplicationService(session)
#     try:
#         if request.status is not None:
#             service.change_status(
#                 user_id=user.user_id,
#                 application_id=application_id,
#                 new_status=request.status,
#             )

#         if request.expected_next_action_date is not None:
#             service.reschedule_next_action(
#                 user_id=user.user_id,
#                 application_id=application_id,
#                 next_date=request.expected_next_action_date,
#             )

#         return None
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
    
# @router.get("/_ping")   
# def ping():
#     return {"ok": True}
