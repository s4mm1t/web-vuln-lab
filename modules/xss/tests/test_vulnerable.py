def test_xss_vulnerable_renders_raw_script(client):
    response = client.get("/xss/vulnerable/", query_string={"q": "<script>alert(1)</script>"})

    assert response.status_code == 200
    assert b"<script>alert(1)</script>" in response.data
