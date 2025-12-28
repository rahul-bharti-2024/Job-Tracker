# app/schemas/common.py
from enum import Enum

class ApplicationStatus(str, Enum):
    SAVED = "SAVED"
    APPLIED = "APPLIED"
    OA = "OA"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    GHOSTED = "GHOSTED"


class ApplicationSource(str, Enum):
    PORTAL = "portal"
    REFERRAL = "referral"
    CAREER_PAGE = "career_page"


class ReminderType(str, Enum):
    DEADLINE = "deadline"
    INTERVIEW = "interview"
    FOLLOW_UP = "follow_up"

