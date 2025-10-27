from sqlalchemy.orm import Session
from app import models , schemas

def get_applications(db:Session, user_id:int):
    return db.query(models.Application).filter(models.Application.user_id==user_id).all()

def get_applications(db:Session , app_id: int:)