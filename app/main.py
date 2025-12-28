from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from app.api.routes.applications import router as applications_router
from app.api.routes.auth import router as auth_router
from app.api.routes.application_tags import router as application_tags_router
from app.api.routes.notes import router as notes_router




app = FastAPI(title="Job Application Tracker API")
security = HTTPBearer()
app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(application_tags_router)
app.include_router(applications_router)
