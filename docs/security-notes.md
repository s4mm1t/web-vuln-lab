# Security Notes

This repository is an educational lab. Some routes are intentionally vulnerable so learners can see how bugs behave and how fixed versions differ.

Do not deploy the vulnerable modules to the internet. Run the lab locally or inside an isolated container.

Recommended local safety practices:

- use Docker or a disposable virtual environment;
- avoid uploading sensitive files during upload demos;
- do not reuse real passwords in the auth demos;
- keep the Flask `SECRET_KEY` value for local training only;
- review each `writeup.md` before extending a vulnerable module.

The fixed modules demonstrate practical defensive patterns, but they are still simplified examples. Production applications also need logging, monitoring, rate limiting, CSRF protection, dependency updates, secret management, and secure deployment configuration.
