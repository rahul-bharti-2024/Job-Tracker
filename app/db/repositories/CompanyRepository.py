from sqlalchemy.orm import Session
from app.db.models.Company import Company
class CompanyRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, company_id: int) -> Company | None:
        return (
            self.session.query(Company)
            .filter(Company.company_id == company_id)
            .one_or_none()
        )
    
    def create(self, company: Company) -> Company:
        self.session.add(company)
        self.session.flush()  # assigns company_id
        return company
    
    def list_all(self,limit:int =100, offset:int=0) -> list[Company]:
        return self.session.query(Company).all()
    
    def delete(self, company_id: int) -> None:
        self.session.query(Company).filter(Company.company_id == company_id).delete()
