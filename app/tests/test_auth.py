def test_register_and_login(client):
    # Register
    r = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "secret123",
        },
    )
    assert r.status_code == 201
    assert "access_token" in r.json()

    # Login
    r = client.post(
        "/auth/login",
        json={
            "email": "test@test.com",
            "password": "secret123",
        },
    )
    assert r.status_code == 200
    assert "access_token" in r.json()
