# Cross-Site Scripting

## What it is

Cross-site scripting, or XSS, happens when an application renders attacker-controlled content as executable HTML or JavaScript in another user's browser.

## Where the bug is

The vulnerable search page renders the query with `safe` in `modules/xss/vulnerable/templates/xss_vulnerable_search.html`:

```jinja2
Search results for: {{ query|safe }}
```

That disables Jinja2 escaping.

## How it appears

Open:

```text
/xss/vulnerable?q=<script>alert(1)</script>
```

The vulnerable page emits a raw `<script>` tag.

## Why the fix works

The fixed page uses normal Jinja2 output:

```jinja2
Search results for: {{ query }}
```

Jinja2 escapes characters such as `<`, `>`, and `"`, so the browser displays the input as text. The fixed route also sends a Content Security Policy:

```text
default-src 'self'; script-src 'self'; object-src 'none'
```

Escaping is the primary fix. CSP is defense in depth.

## XSS types

- Reflected XSS: the payload comes from the current request and is reflected in the response.
- Stored XSS: the payload is saved server-side and shown later to other users.
- DOM XSS: client-side JavaScript reads unsafe data and writes it into the DOM unsafely.

This module demonstrates reflected XSS.

## Extra defenses

- Escape output by context: HTML body, attributes, JavaScript, CSS, and URLs have different rules.
- Avoid marking user input as safe HTML.
- Sanitize rich text with a trusted allowlist sanitizer when HTML input is truly required.
- Add CSP to reduce impact if an escaping bug slips through.
