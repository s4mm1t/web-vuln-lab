def test_idor_fixed_allows_own_profile(client):
    response = client.get("/idor/fixed/", query_string={"id": "1"})

    assert response.status_code == 200
    assert b"Alice" in response.data


def test_idor_fixed_blocks_other_users_profile(client):
    response = client.get("/idor/fixed/", query_string={"id": "2"})

    assert response.status_code == 403
    assert b"bob@example.test" not in response.data
