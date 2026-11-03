# Search and discovery maintenance

Autopilot should be found for interrupted AI work, repeated briefing and
cross-session handoffs. Discovery is not evidence of better outcomes.

## What this repository provides

- A problem-first README, skill description and Codex UI description.
- English/Korean [interrupted-work guide](https://presentjay.github.io/autopilot-skills/when-agent-stops.html)
  and [public-record case](https://presentjay.github.io/autopilot-skills/handoff-example.html).
- Unique page descriptions, canonical URLs, reciprocal language alternatives,
  social previews and a generated [sitemap](https://presentjay.github.io/autopilot-skills/sitemap.xml).
- A Pages build and rendered-output check in the existing CI.

The articles cite existing public evaluation artifacts. They do not claim
a successful cross-session recovery test, cancellation prevention or a reduction
in supervision, execution time or cost.

## After a documentation publication

1. Follow [PUBLISH.md](PUBLISH.md); verify the Pages build and public URLs.
2. In an authorized Google Search Console URL-prefix property for
   `https://presentjay.github.io/autopilot-skills/`, submit
   `https://presentjay.github.io/autopilot-skills/sitemap.xml`. Inspect the landing
   page and the two guides, and request indexing if appropriate. Check existing
   Search generative AI settings and inherited exclusions; inclusion is the default.
   This repository does not hold Search Console credentials or a verification token.
3. Measure search impressions/clicks and, where available, the Generative AI
   performance report. Keep dates and query groups; do not claim an exposure gain
   merely because metadata shipped.
4. Review the existing [skills.sh listing](https://www.skills.sh/presentjay/autopilot-skills/autopilot).
   On 2026-11-03 its HTTP 200 body still described v1. Current source is v2.0.0.
   An author cache refresh API was not found in the official documentation.
   Use the [official contact route](https://www.skills.sh/contact) to request a
   snapshot correction, with the listing, source and release URLs.
   [Correction request #2657](https://github.com/vercel-labs/skills/issues/2657)
   was filed on 2026-11-03; a response or refreshed snapshot is still pending.
   Check that request before sending another; do not reinstall to manufacture ranking events.
5. AgentStack search results retained v0.1.0 wording on the same date. Live access
   was inconclusive (web 404 and TLS EOF); confirm the service and a maintainer
   contact path before asking for a correction.

The host-root `https://presentjay.github.io/robots.txt` returned 404 during the
read-only check. A project-path robots.txt would not control host-root crawling.
Do not modify another repository or add crawler-policy files here to imply it does.
No new accounts, analytics service, submission bot or recurring job is required
by these changes. Do not promise indexing, ranking or AI citations.

## Share a useful case

Use the public-record article as the source. A concise introduction can say:

> If you keep telling Codex to continue or rebuilding the same brief in a new
> session, Autopilot keeps the mission, checked progress and next action together.
> It works with Codex and Claude Code using their existing runtime. The guide
> includes durable-record and explicit-resume prompts; the public case distinguishes
> actual records from untested recovery benefits.

Link to the guide in context. Respect the destination community's rules and
require explicit authorization before posting on someone else's issue, forum
or account. Avoid duplicate promotional replies and fabricated testimonials.

## Primary references

- [Google generative AI search guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Build and submit sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Request a recrawl](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
- [Search generative AI control](https://support.google.com/webmasters/answer/16908024)
- [Skills FAQ](https://www.skills.sh/docs/faq) and [customization](https://www.skills.sh/docs/customize)
- [Agent Skills specification](https://agentskills.io/specification)

The existing Pages deployment remains branch based. See PUBLISH.md for the
reviewed source and publication commit; do not merge a PR without approval.

## Repository metadata applied on 2026-11-03

The existing repository About description now names interrupted work and
cross-session handoffs in Codex and Claude Code. Relevant `session-handoff`,
`long-running-tasks` and `ai-agents` topics were added; the broad
`self-improvement` topic was removed. This improves the accuracy of the public
entry point; search traffic and AI recommendations have not yet been measured.
