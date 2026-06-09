def test_auth_vulnerable_accepts_password_in_query_string(client):
    response = client.get("/auth/vulnerable/", query_string={"username": "admin", "password": "123456"})

    assert response.status_code == 200
    assert b"Logged in as admin" in response.data
    assert b"password" in response.request.query_string
