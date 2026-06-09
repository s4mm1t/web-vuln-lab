import bcrypt

from modules.auth.fixed.app import PASSWORD_HASH


def test_auth_fixed_hash_is_bcrypt_not_plaintext():
    assert PASSWORD_HASH.startswith(b"$2")
    assert b"password123" not in PASSWORD_HASH
    assert bcrypt.checkpw(b"password123", PASSWORD_HASH)


def test_auth_fixed_logs_in_with_post_session_cookie(client):
    response = client.post(
        "/auth/fixed/",
        data={"username": "admin", "password": "password123"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/fixed/profile")
    cookie = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie

    profile = client.get("/auth/fixed/profile")
    assert profile.status_code == 200
    assert b"Welcome, admin" in profile.data
