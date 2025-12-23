"""app.domain.job_application

Minimal domain object representing a job application and status transitions.

This module intentionally keeps things small and framework-free. It uses
`ApplicationStatus` and `can_transition` from `app.domain.application_status`.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from app.domain.application_status import ApplicationStatus, can_transition


class JobApplication:
	"""A minimal domain object for a job application.

	Attributes:
		status: current application status
		expected_next_action_date: optional next action date
	"""

	def __init__(self, status: ApplicationStatus, expected_next_action_date: Optional[date] = None) -> None:
		self.status = status
		self.expected_next_action_date = expected_next_action_date

	def transition_to(self, new_status: ApplicationStatus) -> None:
		"""Attempt to transition to `new_status`.

		Raises `ValueError` if the transition is not allowed.
		"""
		if not can_transition(self.status, new_status):
			raise ValueError(f"Cannot transition from {self.status} to {new_status}")
		self.status = new_status
