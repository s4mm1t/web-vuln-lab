def test_sqli_fixed_rejects_login_bypass(client):
    response = client.post(
        "/sqli/fixed/",
        data={"username": "admin' --", "password": "not-the-password"},
    )

    assert response.status_code == 200
    assert b"Invalid credentials." in response.data
    assert b"Welcome, admin!" not in response.data


def test_sqli_fixed_allows_valid_credentials(client):
    response = client.post(
        "/sqli/fixed/",
        data={"username": "admin", "password": "password123"},
    )

    assert response.status_code == 200
    assert b"Welcome, admin!" in response.data
