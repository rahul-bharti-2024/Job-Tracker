from fastapi import FastAPI
from app.api.routes.job_applications import router as job_applications_router
from app.api.routes import auth


app= FastAPI(title= "Job Tracker MVP")

app.include_router(auth.router)
app.include_router(job_applications_router)
