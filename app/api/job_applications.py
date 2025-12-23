from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.services.JobApplicationService import JobApplicationService
from app.api.schemas.job_applications import(
    CreateApplicationRequest, UpdateApplicationRequest

)

router= APIRouter(prefix="/applications", tags=["job_applications"])

USER_ID=1  # Placeholder for authenticated user ID
@router.post("/")
def create_application(
    request: CreateApplicationRequest,
    session: Session = Depends(get_session),
):
    service= JobApplicationService(session)
    try:
        application= service.create_application(
            user_id= USER_ID,
            **request.model_dump(),
        )
        return application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/")
def list_applications(
    status: str | None = None,
    company_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    print("ENTERED ROUTE")
    service = JobApplicationService(session)
    print("CALLING SERVICE")
    result = service.list_applications(
        user_id=USER_ID,
        status=status,
        company_id=company_id,
        limit=limit,
        offset=offset,
    )
    print("RETURNING")
    return result


@router.get("/{application_id}")
def get_application(
    application_id:int,
    session : Session= Depends(get_session),
):
    service= JobApplicationService(session)
    try:
        application= service.get_application(
            user_id= USER_ID,
            application_id= application_id,
        )
        return application
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    
@router.patch("/{application_id}/status")
def update_application_status(
    application_id:int,
    request: UpdateApplicationRequest,
    session: Session = Depends(get_session),
):
    service= JobApplicationService(session)
    try:
        application= service.update_application_status(
            user_id= USER_ID,
            application_id= application_id,
            status= request.status,
            expected_next_action_date= request.expected_next_action_date,
        )
        return application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/_ping")   
def ping():
    return {"ok": True}
