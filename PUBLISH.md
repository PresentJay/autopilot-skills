# How to publish this repo

This folder is a **standalone repo skeleton** sitting inside the lyon-v1 workspace for convenience. Move it out and turn it into its own GitHub repo to enable `npx skills add`.

## Steps

### 1. Move out of the parent workspace

```bash
mv /Users/ab180/conductor/workspaces/airflux-agent-platform/lyon-v1/autopilot-skills ~/dev/autopilot-skills
cd ~/dev/autopilot-skills
```

(Pick any location you like — `~/dev/`, `~/Code/`, anywhere.)

### 2. Metadata is pre-filled

`package.json`, `README.md`, `PUBLISH.md` already point at `PresentJay/autopilot-skills`. `LICENSE` already has Hyeonjae Jeong as the copyright holder. Edit only if you want to change them.

### 3. Initialize git + push

```bash
git init -b main
git add .
git commit -m "feat: autopilot — universal self-driving mission runner v0.1.0"

# Create the GitHub repo and push (gh CLI):
gh repo create PresentJay/autopilot-skills \
  --public \
  --description "Universal self-driving mission runner for AI coding agents" \
  --source=. \
  --remote=origin \
  --push
```

### 4. Smoke test the install

In a separate project directory:

```bash
cd ~/some-other-project
npx skills add PresentJay/autopilot-skills
```

Verify the SKILL.md landed in your harness's skills directory:

```bash
ls ~/.claude/skills/autopilot/SKILL.md   # Claude Code
ls ~/.codex/skills/autopilot/SKILL.md    # Codex CLI
# etc
```

Then in the harness, run `/autopilot` — boot interview should kick in.

### 5. (Optional) Tag a release

```bash
git tag v0.1.0
git push origin v0.1.0

# Or via gh:
gh release create v0.1.0 --notes "Initial release: autopilot skill v1 (boot interview, 8-phase cycle, safety policy, milestone trail)."
```

GitHub releases give `skills` CLI a clear version target (`npx skills add PresentJay/autopilot-skills@v0.1.0`).

## Versioning the skill itself

`SKILL.md` frontmatter has a `version: 1.0.0` field. When you ship breaking changes, bump it. The `skills` CLI uses this for its own update detection.

Recommended bump rules:
- patch (1.0.0 → 1.0.1) — bug fixes, doc fixes
- minor (1.0.0 → 1.1.0) — new optional question / new tool / non-breaking phase tweak
- major (1.0.0 → 2.0.0) — schema change in mission.md, breaking change in cycle protocol, removed feature

Keep `package.json` `version` in sync if you'll later publish to npm.

## Optional: npm publish (skip unless you want a branded CLI)

The `skills add` flow does NOT require npm publish — it pulls from GitHub. Publish to npm only if you decide to add a custom CLI later (impeccable-style branding). For v1, skip this step.

If you do publish:

```bash
npm login
npm publish --access public
```

Pick a unique package name (`autopilot-skills` may be taken; check with `npm view <name>`). Recommend something like `@<your-scope>/autopilot-skills`.

## After publishing — link back

Once the repo is live, add a one-liner to the airflux-agent-platform README pointing to the new repo as the canonical autopilot source. That replaces the local `.claude/commands/autopilot.md` which was the v0 we shipped earlier.
