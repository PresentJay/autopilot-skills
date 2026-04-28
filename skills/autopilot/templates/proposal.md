<!-- Write to proposals/<id>.md after Phase 3 ANALYZE -->

# Proposal: <id> — <title>

**Discovered by**: <Phase 1 tool>
**Priority**: <P1 | P2>
**Created**: <ISO>

## What
<2-3 lines — what to change>

## Evidence (auto-discovery output, ≤20 lines)

```
<excerpt of tool output that triggered this proposal>
```

## Impact analysis

- **Files affected**: <list>
- **Modules / users affected**: <list or "none">
- **Reversibility**: reversible | partially reversible (config) | irreversible
- **Conflicts with other proposals**: <list or "none">

## Plan

- **Change scope**: <files, expected lines>
- **Verify**: <build / test / lint / smoke commands>
- **Rollback**: <git restore | feature flag | config revert>
- **Dry-run available?**: yes | no

## Risk
- <known risks, one per line>

## Acceptance
- <explicit pass/fail criteria — Phase 6 VERIFY decides on this>
