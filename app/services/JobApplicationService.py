from typing import Optional, List
from datetime import date
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.repositories.job_application import JobApplicationRepository
from app.db.models.job_application import JobApplication
from app.domain.application_status import ApplicationStatus, parse_status
from app.domain.job_application import JobApplication as DomainJobApplication

logger = logging.getLogger(__name__)


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
        job_posting_url: Optional[str],
        role_title: Optional[str],
        status: str,
        date_applied: Optional[date],
        expected_next_action_date: Optional[date],
    ) -> JobApplication:
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
            if not self.session.in_transaction():
                with self.session.begin():
                    created = self.job_repo.create(app)
                    logger.debug(
                        "Created job application id=%s user=%s company=%s",
                        getattr(created, "id", None),
                        user_id,
                        company_id,
                    )
                    return created
            else:
                created = self.job_repo.create(app)
                logger.debug(
                    "Created job application id=%s user=%s company=%s",
                    getattr(created, "id", None),
                    user_id,
                    company_id,
                )
                return created
        except IntegrityError:
            logger.debug(
                "Duplicate job application create attempt user=%s company=%s external=%s",
                user_id,
                company_id,
                external_job_id,
            )
            raise ValueError("Job application already exists")

    def list_applications(
        self,
        *,
        user_id: int,
        status: Optional[str] = None,
        company_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[JobApplication]:
        return self.job_repo.list_by_user(
            user_id=user_id,
            status=status,
            company_id=company_id,
            limit=limit,
            offset=offset,
        )

    def get_application(self, *, user_id: int, application_id: int) -> JobApplication:
        app = self.job_repo.get_by_id_for_user(
            application_id=application_id,
            user_id=user_id,
        )

        if app is None:
            raise ValueError("Application not found")

        return app

    def change_status(self, *, user_id: int, application_id: int, new_status: str) -> None:
        # Use explicit transaction if none is active to avoid nested transaction errors in tests
        if not self.session.in_transaction():
            with self.session.begin():
                app = self.job_repo.get_by_id_for_user(
                    application_id=application_id,
                    user_id=user_id,
                    for_update=True,
                )

                if app is None:
                    raise ValueError("Application not found")

                try:
                    current_enum = parse_status(app.status)
                except ValueError:
                    raise ValueError("Unknown current status in DB")

                try:
                    target_enum = parse_status(new_status)
                except ValueError:
                    raise ValueError("Invalid target status")

                if current_enum == ApplicationStatus.REJECTED:
                    raise ValueError("Cannot change status of rejected application")

                if current_enum == target_enum:
                    return

                domain_obj = DomainJobApplication(status=current_enum, expected_next_action_date=app.expected_next_action_date)
                try:
                    domain_obj.transition_to(target_enum)
                except ValueError as exc:
                    raise ValueError(str(exc))

                self.job_repo.update_status(application_id, target_enum.value)
                logger.debug("Updated status application=%s -> %s", application_id, target_enum.value)
        else:
            app = self.job_repo.get_by_id_for_user(
                application_id=application_id,
                user_id=user_id,
                for_update=True,
            )

            if app is None:
                raise ValueError("Application not found")

            try:
                current_enum = parse_status(app.status)
            except ValueError:
                raise ValueError("Unknown current status in DB")

            try:
                target_enum = parse_status(new_status)
            except ValueError:
                raise ValueError("Invalid target status")

            if current_enum == ApplicationStatus.REJECTED:
                raise ValueError("Cannot change status of rejected application")

            if current_enum == target_enum:
                return

            domain_obj = DomainJobApplication(status=current_enum, expected_next_action_date=app.expected_next_action_date)
            try:
                domain_obj.transition_to(target_enum)
            except ValueError as exc:
                raise ValueError(str(exc))

            self.job_repo.update_status(application_id, target_enum.value)
            logger.debug("Updated status application=%s -> %s", application_id, target_enum.value)

    def reschedule_next_action(self, *, user_id: int, application_id: int, next_date: Optional[date]) -> None:
        if not self.session.in_transaction():
            with self.session.begin():
                app = self.job_repo.get_by_id_for_user(
                    application_id=application_id,
                    user_id=user_id,
                    for_update=True,
                )

                if app is None:
                    raise ValueError("Application not found")

                try:
                    current_enum = parse_status(app.status)
                except ValueError:
                    raise ValueError("Unknown current status in DB")

                if current_enum == ApplicationStatus.REJECTED:
                    raise ValueError("Rejected applications cannot be rescheduled")

                self.job_repo.update_expected_next_action_date(application_id, next_date)
                logger.debug(
                    "Rescheduled next action application=%s next_date=%s",
                    application_id,
                    next_date,
                )
        else:
            app = self.job_repo.get_by_id_for_user(
                application_id=application_id,
                user_id=user_id,
                for_update=True,
            )

            if app is None:
                raise ValueError("Application not found")

            try:
                current_enum = parse_status(app.status)
            except ValueError:
                raise ValueError("Unknown current status in DB")

            if current_enum == ApplicationStatus.REJECTED:
                raise ValueError("Rejected applications cannot be rescheduled")

            self.job_repo.update_expected_next_action_date(application_id, next_date)
            logger.debug(
                "Rescheduled next action application=%s next_date=%s",
                application_id,
                next_date,
            )

    def delete_application(self, *, user_id: int, application_id: int) -> None:
        if not self.session.in_transaction():
            with self.session.begin():
                app = self.job_repo.get_by_id_for_user(
                    application_id=application_id,
                    user_id=user_id,
                    for_update=True,
                )

                if app is None:
                    raise ValueError("Application not found")

                self.job_repo.delete(application_id)
                logger.debug("Deleted application=%s", application_id)
        else:
            app = self.job_repo.get_by_id_for_user(
                application_id=application_id,
                user_id=user_id,
                for_update=True,
            )

            if app is None:
                raise ValueError("Application not found")

            self.job_repo.delete(application_id)
            logger.debug("Deleted application=%s", application_id)
