def test_sqli_vulnerable_allows_login_bypass(client):
    response = client.post(
        "/sqli/vulnerable/",
        data={"username": "admin' --", "password": "not-the-password"},
    )

    assert response.status_code == 200
    assert b"Welcome, admin!" in response.data
    assert b"admin&#39; --" in response.data
