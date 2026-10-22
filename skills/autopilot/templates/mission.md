# Autopilot Mission

**Created**: <ISO timestamp>
**Mode**: active <!-- active | active-manual | paused | done | aborted -->
**Mission ID**: <stable identifier>

## Outcome and deliverables
<What must be true and what the user should receive.>

## Scope and authorization
- Targets: <paths, modules, document IDs/edit ranges, or research questions>
- Allowed actions: <established user authorization>
- Forbidden scope: <project/user boundaries>
- Existing edits or target revision: <baseline to preserve>

## Acceptance criteria
- C1: <observable result and decisive verification method>
<!-- Add independent criteria for each required deliverable. -->

## Execution and stopping
- Kind: finite <!-- finite | monitor -->
- Invocation: checkpoint <!-- checkpoint | run-once | native-goal -->
- Checkpoint/time/budget limits: <only if specified by the user>
- Stop or handoff when: <completion, explicit stop, unresolved access/conflict>
- Schedule: none <!-- confirmed host schedule ID, next run, cadence if authorized -->

## Storage
- journal_root: .autopilot.log/
- milestones_root: .autopilot.milestones/

## Verification and evidence
<Relevant commands, source checks, document review, or before/after measurements.>
<Identify which artifact version each check covers. No universal npm/Git steps.>

## Lessons and remaining work
<Reproducible findings, unresolved criteria, and next action.>
