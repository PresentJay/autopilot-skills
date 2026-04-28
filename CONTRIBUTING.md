# Contributing to autopilot-skills

Thank you for considering a contribution. autopilot is a self-driving mission runner for AI coding agents — small, sharp changes are welcome; large new features should be discussed in an issue first.

## Getting started

```bash
git clone https://github.com/PresentJay/autopilot-skills
cd autopilot-skills
npx -y skills add . --copy --all -g   # install the local copy globally for dev
```

Edit `skills/autopilot/SKILL.md`, then re-sync:

```bash
npx -y skills experimental_sync -y
```

## Propose a change

1. Open an issue describing the change (use the bug / feature / question template).
2. Fork + branch (`feat/your-change`, `fix/your-issue-number`).
3. Open a PR. Reference the issue.

## SKILL.md frontmatter rules

- `name` — lowercase, hyphens only.
- `description` — under 500 chars, must include trigger keywords (e.g. `자율주행`, `autopilot`, `self-drive`).
- `version` — semver. Bump on every change.

## Commit format

Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`. Subject ≤ 70 chars; body explains *why*.

## PR checklist

- [ ] frontmatter valid (`name`, `description`, `version`)
- [ ] `version` bumped (semver)
- [ ] `CHANGELOG.md` entry under "Unreleased"
- [ ] README updated if user-facing
- [ ] No project-specific paths or PII

## License

By contributing you agree your work is MIT-licensed (see `LICENSE`).

## Code of Conduct

This project follows the Contributor Covenant 2.1 — see `CODE_OF_CONDUCT.md`.
