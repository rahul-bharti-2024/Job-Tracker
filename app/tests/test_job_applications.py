# def auth_header(token: str):
#     return {"Authorization": f"Bearer {token}"}


# def test_user_can_create_and_list_applications(client, company):
#     # Register user
#     r = client.post(
#         "/auth/register",
#         json={
#             "username": "user1",
#             "email": "user1@test.com",
#             "password": "pass123",
#         },
#     )
#     assert r.status_code == 201
#     token = r.json()["access_token"]

#     # Create application
#     r = client.post(
#         "/applications/",
#         headers=auth_header(token),
#         json={
#             "company_id": company.company_id,
#             "external_job_id": "job-123",
#             "status": "APPLIED",
#         },
#     )
#     assert r.status_code == 201

#     # List applications
#     r = client.get(
#         "/applications/",
#         headers=auth_header(token),
#     )
#     assert r.status_code == 200
#     assert len(r.json()) == 1
