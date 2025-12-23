from enum import Enum
from typing import Dict, Set


class ApplicationStatus(Enum):
    APPLIED = "APPLIED"
    OA = "OA"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    RESCINDED = "RESCINDED"


ALLOWED_TRANSITIONS: Dict[ApplicationStatus, Set[ApplicationStatus]] = {
    ApplicationStatus.APPLIED: {
        ApplicationStatus.OA,
        ApplicationStatus.INTERVIEW,
        ApplicationStatus.OFFER,
        ApplicationStatus.REJECTED,
        ApplicationStatus.WITHDRAWN,
    },
    
    ApplicationStatus.OA: {
        ApplicationStatus.INTERVIEW,
        ApplicationStatus.OFFER,
        ApplicationStatus.REJECTED,
        ApplicationStatus.WITHDRAWN,
    },
    ApplicationStatus.INTERVIEW: {
        ApplicationStatus.OFFER,
        ApplicationStatus.REJECTED,
        ApplicationStatus.WITHDRAWN,
    },
    ApplicationStatus.OFFER: {
        ApplicationStatus.ACCEPTED,
        ApplicationStatus.WITHDRAWN,
        ApplicationStatus.RESCINDED,
    },
    ApplicationStatus.ACCEPTED: set(),
    ApplicationStatus.REJECTED: set(),
    ApplicationStatus.WITHDRAWN: set(),
    ApplicationStatus.RESCINDED: set(),
}


def can_transition(from_status: ApplicationStatus, to_status: ApplicationStatus) -> bool:
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())
