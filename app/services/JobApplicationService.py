from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date

from app.db.repositories.JobApplicationRepository import JobApplicationRepository
from app.db.models.JobApplication import JobApplication


class JobApplicationService:
    def __init__(self, session: Session):
        self.session = session
        self.job_repo = JobApplicationRepository(session)

    def create_application(
        self,
        *,
        user_id: int,
        company_id: int,
        external_job_id: str,
        job_posting_url: str | None,
        role_title: str | None,
        status: str,
        date_applied: date | None,
        expected_next_action_date: date | None,
    ) -> JobApplication:

        with self.session.begin():
            if self.job_repo.exists(user_id, company_id, external_job_id):
                raise ValueError("Job application already exists")

            app = JobApplication(
                user_id=user_id,
                company_id=company_id,
                external_job_id=external_job_id,
                job_posting_url=job_posting_url,
                role_title=role_title,
                status=status,
                date_applied=date_applied,
                expected_next_action_date=expected_next_action_date,
            )

            try:
                return self.job_repo.create(app)
            except IntegrityError:
                raise ValueError("Job application already exists")

    def list_applications(
        self,
        *,
        user_id: int,
        status: str | None = None,
        company_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ):
        return self.job_repo.list_by_user(
            user_id=user_id,
            status=status,
            company_id=company_id,
            limit=limit,
            offset=offset,
        )

    def get_application(
        self,
        *,
        user_id: int,
        application_id: int,
    ):
        app = self.job_repo.get_by_id_for_user(
            application_id=application_id,
            user_id=user_id,
        )

        if app is None:
            raise ValueError("Application not found")

        return app

    def change_status(
        self,
        *,
        user_id: int,
        application_id: int,
        new_status: str,
    ) -> None:

        with self.session.begin():
            app = self.job_repo.get_by_id_for_user(
                application_id=application_id,
                user_id=user_id,
                for_update=True,
            )

            if app is None:
                raise ValueError("Application not found")

            if app.status == "rejected":
                raise ValueError("Cannot change status of rejected application")

            if app.status == new_status:
                return

            self.job_repo.update_status(application_id, new_status)

    def reschedule_next_action(
        self,
        *,
        user_id: int,
        application_id: int,
        next_date: date | None,
    ) -> None:

        with self.session.begin():
            app = self.job_repo.get_by_id_for_user(
                application_id=application_id,
                user_id=user_id,
                for_update=True,
            )

            if app is None:
                raise ValueError("Application not found")

            if app.status == "rejected":
                raise ValueError("Rejected applications cannot be rescheduled")

            self.job_repo.update_expected_next_action_date(
                application_id,
                next_date,
            )

    def delete_application(
        self,
        *,
        user_id: int,
        application_id: int,
    ) -> None:

        with self.session.begin():
            app = self.job_repo.get_by_id_for_user(
                application_id=application_id,
                user_id=user_id,
                for_update=True,
            )

            if app is None:
                raise ValueError("Application not found")

            self.job_repo.delete(application_id)
