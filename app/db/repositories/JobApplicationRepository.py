from datetime import date
from typing import Optional, Sequence
from sqlalchemy.orm import Session

from app.db.models.JobApplication import JobApplication


class JobApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    # ============================================================
    # Creation
    # ============================================================

    def create(self, app: JobApplication) -> JobApplication:
        """
        Create a new job application.

        Enforces uniqueness via DB constraint.
        """
        self.session.add(app)
        self.session.flush()  # assigns application_id
        return app

    def exists(
        self,
        user_id: int,
        company_id: int,
        external_job_id: str,
    ) -> bool:
        """
        Logical identity existence check.
        """
        return (
            self.session.query(JobApplication.application_id)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.company_id == company_id,
                JobApplication.external_job_id == external_job_id,
            )
            .first()
            is not None
            
        )

    # ============================================================
    # Reads
    # ============================================================

    def get_by_id(
        self,
        application_id: int,
        *,
        for_update: bool = False,
    ) -> Optional[JobApplication]:
        """
        Fetch by physical identity.
        """
        query = self.session.query(JobApplication).filter(
            JobApplication.application_id == application_id
        )

        if for_update:
            query = query.with_for_update()

        return query.one_or_none()


    def get_by_id_for_user(
        self,
        application_id: int,
        user_id: int,
        *,
        for_update: bool = False,
    ) -> Optional[JobApplication]:
        query = self.session.query(JobApplication).filter(
            JobApplication.application_id == application_id,
            JobApplication.user_id == user_id,
        )

        if for_update:
            query = query.with_for_update()

        return query.one_or_none()


    def list_by_user(
        self,
        user_id: int,
        *,
        status: Optional[str] = None,
        company_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[JobApplication]:
        """
        List applications for a user with optional filters.
        """
        query = self.session.query(JobApplication).filter(
            JobApplication.user_id == user_id
        )

        if status is not None:
            query = query.filter(JobApplication.status == status)

        if company_id is not None:
            query = query.filter(JobApplication.company_id == company_id)

        return (
            query.order_by(JobApplication.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    # ============================================================
    # Lifecycle updates (ONLY mutable fields)
    # ============================================================

    def update_lifecycle(
        self,
        application_id: int,
        *,
        status: Optional[str] = None,
        expected_next_action_date: Optional[date] = None,
    ) -> None:
        """
        Atomic update of lifecycle fields.
        Only allowed mutable fields can be modified.
        """
        update_values = {}

        if status is not None:
            update_values["status"] = status

        if expected_next_action_date is not None:
            update_values["expected_next_action_date"] = expected_next_action_date

        if not update_values:
            return  # no-op

        self.session.query(JobApplication).filter(
            JobApplication.application_id == application_id
        ).update(
            update_values,
            synchronize_session=False,
        )

    # Convenience wrappers (optional)
    def update_status(self, application_id: int, status: str) -> None:
        self.update_lifecycle(application_id, status=status)

    def update_expected_next_action_date(
        self,
        application_id: int,
        next_date: Optional[date],
    ) -> None:
        self.update_lifecycle(
            application_id,
            expected_next_action_date=next_date,
        )

    # ============================================================
    # Deletion (only if allowed by product)
    # ============================================================

    def delete(self, application_id: int) -> None:
        self.session.query(JobApplication).filter(
            JobApplication.application_id == application_id
        ).delete()
