# Web Vulnerability Lab

Educational Flask lab demonstrating common web vulnerabilities and their secure fixes.

This project is intended for local learning only. Each module contains a deliberately vulnerable implementation, a fixed implementation, a writeup, and regression tests that prove the security difference.

## Modules

| Module | Vulnerable Demo | Fixed Demo | Topic |
|---|---|---|---|
| SQL Injection | `/sqli/vulnerable` | `/sqli/fixed` | Parameterized queries |
| XSS | `/xss/vulnerable` | `/xss/fixed` | Output escaping and CSP |
| File Upload | `/upload/vulnerable` | `/upload/fixed` | File validation |
| Broken Auth | `/auth/vulnerable` | `/auth/fixed` | Sessions and password hashing |
| IDOR | `/idor/vulnerable` | `/idor/fixed` | Authorization checks |

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app.main run --debug
```

Open http://localhost:5000.

## Docker

```bash
docker compose up --build
```

Open http://localhost:5000.

## Tests

```bash
pytest
```

The tests intentionally prove both sides:

- vulnerable SQLi allows a login bypass;
- fixed SQLi rejects the same payload;
- vulnerable XSS renders raw HTML;
- fixed XSS escapes output and sends CSP;
- vulnerable upload accepts an HTML file;
- fixed upload rejects dangerous or mismatched files;
- vulnerable auth accepts credentials in the URL;
- fixed auth uses POST, bcrypt, and sessions;
- vulnerable IDOR leaks another user's profile;
- fixed IDOR returns `403`.

## Screenshots

Screenshots are stored in `docs/screenshots/`:

- dashboard desktop and mobile views;
- SQLi vulnerable bypass and fixed blocked login;
- XSS vulnerable and fixed search pages;
- upload validation error;
- fixed IDOR `403`.

## Structure

```text
app/
  main.py
  templates/
  static/
modules/
  sqli/
    vulnerable/
    fixed/
    writeup.md
    tests/
  xss/
  upload/
  auth/
  idor/
docs/
  screenshots/
  security-notes.md
```

## Safety

The vulnerable modules are intentionally unsafe. Run this project only locally or in an isolated environment. Do not deploy it to the public internet.
