# import pytest
# from app.domain.application_status import parse_status, ApplicationStatus
# from app.domain.job_application import JobApplication


# def test_parse_status_accepts_common_variants():
#     assert parse_status("applied") == ApplicationStatus.APPLIED
#     assert parse_status(" Applied ") == ApplicationStatus.APPLIED
#     assert parse_status("APPLIED") == ApplicationStatus.APPLIED
#     assert parse_status("oa") == ApplicationStatus.OA
#     assert parse_status("OA") == ApplicationStatus.OA
#     assert parse_status("interview") == ApplicationStatus.INTERVIEW
#     assert parse_status("offer") == ApplicationStatus.OFFER


# def test_parse_status_rejects_unknown():
#     with pytest.raises(ValueError):
#         parse_status("not-a-status")


# def test_domain_transition_allowed_and_disallowed():
#     ja = JobApplication(status=ApplicationStatus.APPLIED)
#     ja.transition_to(ApplicationStatus.OA)
#     assert ja.status == ApplicationStatus.OA

#     ja2 = JobApplication(status=ApplicationStatus.ACCEPTED)
#     with pytest.raises(ValueError):
#         ja2.transition_to(ApplicationStatus.OFFER)
