def test_xss_fixed_escapes_script_and_sets_csp(client):
    response = client.get("/xss/fixed/", query_string={"q": "<script>alert(1)</script>"})

    assert response.status_code == 200
    assert b"<script>alert(1)</script>" not in response.data
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.data
    assert response.headers["Content-Security-Policy"].startswith("default-src 'self'")
