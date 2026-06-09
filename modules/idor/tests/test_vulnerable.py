def test_idor_vulnerable_exposes_another_users_profile(client):
    response = client.get("/idor/vulnerable/", query_string={"id": "2"})

    assert response.status_code == 200
    assert b"Bob" in response.data
    assert b"bob@example.test" in response.data
