# Insecure Direct Object Reference

## What it is

IDOR happens when an application exposes an object identifier and fails to verify that the current user is allowed to access that object.

IDOR is not simply "missing login." It is missing authorization for a specific object.

## Where the bug is

The vulnerable profile page reads an id from the URL and returns that profile:

```text
/idor/vulnerable?id=2
```

The route sets the current user to user 1 for the demo, but it still returns profile 2 when requested.

## How it appears

Open:

```text
/idor/vulnerable?id=1
/idor/vulnerable?id=2
```

Both profiles are visible to the same logged-in user.

## Why the fix works

The fixed route loads the requested object and verifies ownership:

```python
if profile_data["owner_id"] != session["user_id"]:
    abort(403)
```

The URL can contain an id, but authorization is decided by trusted server-side session state and object ownership.

## Extra defenses

- Check authorization on every object access.
- Prefer object lookup helpers that include user scope by default.
- Log authorization failures.
- Use unpredictable identifiers only as defense in depth, not as the primary authorization control.
