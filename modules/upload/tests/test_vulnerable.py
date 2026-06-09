from io import BytesIO


def test_upload_vulnerable_accepts_html_file(client):
    response = client.post(
        "/upload/vulnerable/",
        data={"file": (BytesIO(b"<script>alert(1)</script>"), "payload.html")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Saved payload.html" in response.data

    uploaded = client.get("/upload/vulnerable/files/payload.html")
    assert uploaded.status_code == 200
    assert b"<script>alert(1)</script>" in uploaded.data
