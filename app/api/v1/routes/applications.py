
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal

from app.models import Application, tag
from app.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])

def get_db():
    db= SessionLocal()
    try:
        yeild(db)#
    finally :
        db.close()

