from fastapi import FastAPI
from app.api.job_applications import router as job_applications_router
app= FastAPI(title= "Job Tracker MVP")

app.include_router(job_applications_router)
