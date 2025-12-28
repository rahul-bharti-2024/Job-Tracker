# app/services/status_rules.py
from app.schemas.common import ApplicationStatus

ALLOWED_TRANSITIONS = {
    ApplicationStatus.SAVED: {
        ApplicationStatus.APPLIED,
    },
    ApplicationStatus.APPLIED: {
        ApplicationStatus.OA,
        ApplicationStatus.INTERVIEW,
        ApplicationStatus.REJECTED,
        ApplicationStatus.GHOSTED,
    },
    ApplicationStatus.OA: {
        ApplicationStatus.INTERVIEW,
        ApplicationStatus.REJECTED,
    },
    ApplicationStatus.INTERVIEW: {
        ApplicationStatus.OFFER,
        ApplicationStatus.REJECTED,
    },
    ApplicationStatus.OFFER: set(),
    ApplicationStatus.REJECTED: set(),
    ApplicationStatus.GHOSTED: set(),
}
