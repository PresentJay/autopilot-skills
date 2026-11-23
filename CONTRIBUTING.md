# Contributing

Autopilot aims to make a mission easy to carry forward across code, research,
and documents. Help us reduce repeated briefing, missed requirements, and needless
supervision. More process is useful only when it fixes an observed problem.

English is the shared documentation language. Issues and discussion in Korean,
Japanese, or Chinese are also welcome; include an English summary when possible.
You do not need to be a native English speaker to contribute.

## Find a useful change

Start with [ROADMAP.md](ROADMAP.md) and linked issues. Bug reports, realistic
fixtures, translations, and measured simplifications are welcome. For a large
change, discuss the concrete failure and proposed scope in an issue first so
maintainers can help avoid duplicate work. Small fixes can go straight to a PR.

Report your agent, model, skill revision, invocation, expected outcome, and actual
artifact. Redact private data. Do not publish credentials or raw private transcripts.

## Make and verify a change

1. Fork the repository and branch from `main` (or the explicitly named preview
   branch when contributing to a preview).
2. Read the relevant skill references, templates, and callers. Keep the change
   focused on the reported failure.
3. Run the existing checks:

   ```sh
   python3 scripts/validate_package.py
   python3 -m unittest discover -s tests -v
   ```

4. For behavior changes, include a small realistic fixture and inspect its actual
   output. For performance claims, compare against a strong native-goal baseline
   with the same model, inputs, tools, and limits. Record failures as well as wins.
5. Update affected documentation. English, Korean, Chinese, and Japanese pages
   must agree on release status, supported behavior, and evidence limitations.
6. Open a focused PR using the template. Maintainers review and merge changes.

Use a Conventional Commit title of at most 70 characters. Add a changelog note
for user-visible behavior changes. Maintainers coordinate version bumps; a typo
fix does not require a release number change.

## Preserve the contract

- Keep `metadata.version`, package.json, and release notes aligned.
- Preserve pre-existing edits and interrupted work; never recover with blanket
  restore/clean/reset.
- Distinguish no changes, blocked access, and verified completion.
- Keep the skill entrypoint short and load details only when needed.
- Keep the user's scope and authorization. A mission is not permission to merge,
  publish, send, or expand access.
- Use native execution facilities. Propose a new runtime or MCP dependency only
  with a demonstrated gap and a comparison against the simpler option.

## Evaluation and publication

See [evals/README.md](evals/README.md) for the bounded pilot, raw-input fixtures,
and limits. Live evaluations are opt-in and never run in public PR CI. Do not
claim a speedup from one run or treat a passing state record as proof of quality.

The source of the website is `docs/`. Preview it with Jekyll or review the static
landing pages, then follow [PUBLISH.md](PUBLISH.md) for the publication branch.
Check desktop, mobile, keyboard focus, language links, and copy controls after a
site change.

Contributions are MIT-licensed. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and
[SECURITY.md](SECURITY.md).
