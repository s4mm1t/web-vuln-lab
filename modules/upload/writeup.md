# File Upload

## What it is

File upload vulnerabilities happen when an application accepts, stores, or serves uploaded files without enough validation and isolation.

## Where the bug is

The vulnerable upload route in `modules/upload/vulnerable/app.py` saves the original filename directly:

```python
destination = upload_root() / uploaded.filename
uploaded.save(destination)
```

It accepts any extension and exposes files through `/upload/vulnerable/files/<filename>`.

## How it appears

An attacker can upload files such as:

- `payload.html` with JavaScript;
- `payload.svg` with scriptable content;
- huge files that consume disk space;
- names crafted for path traversal attempts.

## Why the fix works

The fixed route combines several controls:

- extension allowlist for `.png`, `.jpg`, and `.jpeg`;
- magic-byte detection for PNG and JPEG;
- `secure_filename` before inspecting the submitted name;
- generated UUID storage names;
- Flask `MAX_CONTENT_LENGTH` size limit;
- storage outside public routes.

This is stronger than extension checks alone because a file named `image.jpg` may still contain HTML or scriptable content.

## Extra defenses

- Store uploads in object storage or a non-executable private directory.
- Serve downloaded files with safe `Content-Type` and `Content-Disposition`.
- Virus scan files when appropriate.
- Strip metadata from images if privacy matters.
- Enforce quotas and rate limits.
