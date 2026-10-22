# Publishing Autopilot

The skill is installed from this GitHub repository. No npm publish is required.
V2 is an unreleased preview on `improve/codex-missions-v2`; `main` still contains
v1.3 until the maintainer reviews and merges the PR. Do not tag a preview as a
stable release or imply that the default install already has preview behavior.

## Validate a candidate

1. Run `python3 scripts/validate_package.py` and `python3 -m unittest discover -s tests -v`.
2. Check discovery with `npx -y skills add . --list` and inspect `npm pack --dry-run`.
3. Review affected behavior with an isolated fixture. Live model runs are opt-in;
   publish conditions, limitations, and failures alongside results.
4. Check migration notes and confirm that existing missions are preserved.
5. Keep `metadata.version`, package.json, and changelog versions aligned. The v2
   changelog remains under Unreleased until an actual release is approved.

Review and merge are separate maintainer decisions. After an authorized release,
the existing semver-tag workflow creates GitHub release notes. Do not silently
update an installed skill during a mission; back it up and validate the update.

## Publish the website

The source is `docs/`. GitHub Pages builds Jekyll from the root of `gh-pages`.
This lets a clearly labeled preview be published without merging its source PR.
The site uses the existing GitHub-hosted Jekyll build, with no new service or
credentials in the repository.

From a reviewed source checkout, use a fresh temporary clone of the publication
branch. Inspect the diff before pushing:

```sh
pages_dir=$(mktemp -d)
git clone --branch gh-pages --single-branch https://github.com/PresentJay/autopilot-skills.git "$pages_dir"
rsync -a --delete --exclude=.git docs/ "$pages_dir/"
git -C "$pages_dir" diff --stat
git -C "$pages_dir" add .
git -C "$pages_dir" commit -m "docs: publish reviewed site"
git -C "$pages_dir" push origin gh-pages
```

Run this with a maintainer's authenticated Git client. A push made using the
Actions `GITHUB_TOKEN` does not trigger this branch-based Pages build. Do not
add such an automation without changing the deployment method deliberately.

After publication, inspect the Pages build status and the public site:

```sh
gh api repos/PresentJay/autopilot-skills/pages/builds/latest --jq .status
```

Check English/Korean/Japanese/Chinese landing pages, installation commands,
evidence and documentation links, desktop/mobile layout, keyboard focus, and
copy controls. Keep preview notices and branch installation instructions until
the corresponding source is released. Record the source and publication commit
in the PR or deployment notes. Roll back by reverting the publication commit;
do not force-push away the publication history.

Site: https://presentjay.github.io/autopilot-skills/
