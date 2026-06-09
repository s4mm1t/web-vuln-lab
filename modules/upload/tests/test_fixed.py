from io import BytesIO


def test_upload_fixed_rejects_html_file(client):
    response = client.post(
        "/upload/fixed/",
        data={"file": (BytesIO(b"<script>alert(1)</script>"), "payload.html")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Only .png, .jpg, and .jpeg files are allowed." in response.data


def test_upload_fixed_rejects_mismatched_extension(client):
    response = client.post(
        "/upload/fixed/",
        data={"file": (BytesIO(b"<html>not really an image</html>"), "photo.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"does not look like a PNG or JPEG" in response.data


def test_upload_fixed_accepts_png_and_renames_file(client):
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
    response = client.post(
        "/upload/fixed/",
        data={"file": (BytesIO(png), "profile.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Upload accepted" in response.data
    assert b"profile.png" not in response.data
    assert b".png" in response.data
