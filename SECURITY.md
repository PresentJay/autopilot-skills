# Security Policy

## Supported versions

Only the latest minor release is supported. autopilot-skills uses semver — security fixes go to the latest tag.

## Reporting a vulnerability

Email **hyeonjae@ab180.co** with subject `[autopilot-skills] security`. Please include:

- the affected version (`SKILL.md` frontmatter `version`)
- reproduction steps
- expected vs actual behavior

Do **not** open a public issue for security reports.

Acknowledgement within 72 hours; fix or mitigation timeline within 7 days for high-severity issues.

## Out of scope

- vulnerabilities in third-party AI harnesses (Claude Code, Codex, etc.) — report those upstream
- mission misconfiguration by users (forbidden zones not set, risk tier too high) — that is the user's responsibility, not a skill bug
