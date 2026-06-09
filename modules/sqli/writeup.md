# SQL Injection

## What it is

SQL injection happens when user-controlled input is placed directly into SQL text. The database then treats part of the input as executable query logic instead of plain data.

## Where the bug is

The vulnerable login builds SQL with an f-string in `modules/sqli/vulnerable/app.py`:

```python
sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

If the username is `admin' --`, the rest of the password condition is commented out.

## How it appears

Submit:

- username: `admin' --`
- password: anything

The vulnerable version logs in as `admin` without knowing the password.

## Why the fix works

The fixed version uses a parameterized query:

```python
conn.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password),
)
```

The SQL structure and the user data are sent separately. The database treats `admin' --` as a literal username value, not as query syntax.

## Extra defenses

- Use parameterized queries or an ORM for every database access.
- Keep database accounts least-privileged.
- Avoid leaking SQL errors to users.
- Validate input for business rules, but do not rely on manual quote filtering for SQLi protection.
