# Broken Authentication

## What it is

Broken authentication covers login and session flaws that let credentials leak, sessions be bypassed, or passwords be stored unsafely.

## Where the bug is

The vulnerable route accepts credentials in the query string:

```text
/auth/vulnerable?username=admin&password=123456
```

It also compares plaintext passwords from an in-memory dictionary and does not create a real authenticated session.

## How it appears

Passwords in URLs can leak through:

- browser history;
- server and proxy logs;
- screenshots;
- Referer headers when the user clicks away.

## Why the fix works

The fixed route uses POST, verifies a bcrypt password hash, and stores authenticated identity in Flask `session`.

Bcrypt is used for password hashing, not encryption. Hashing is one-way: the app verifies a submitted password by hashing/checking it, but it cannot decrypt the stored value back into the original password.

The app also configures session cookie flags:

- `HttpOnly` to keep cookies away from JavaScript;
- `SameSite=Lax` to reduce cross-site request leakage;
- `Secure` should be enabled when serving over HTTPS.

## Extra defenses

- Add CSRF protection for state-changing forms.
- Rate-limit login attempts.
- Require strong passwords or passkeys.
- Rotate secrets and keep `SECRET_KEY` out of source control in production.
- Monitor suspicious login behavior.
