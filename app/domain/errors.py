class DomainError(Exception):
    """Base class for domain-level errors."""


class NotFoundError(DomainError):
    pass


class ForbiddenError(DomainError):
    pass


class InvalidStatusTransitionError(DomainError):
    def __init__(self, from_status, to_status):
        super().__init__(f"Cannot transition from {from_status} to {to_status}")


class InvalidRescheduleError(DomainError):
    def __init__(self, date):
        super().__init__(f"Cannot reschedule to past date: {date}")
