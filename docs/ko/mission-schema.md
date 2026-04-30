---
title: 미션 스키마
---

# 미션 스키마

각 섹션은 부트업 인터뷰에서 답하는 한 문항입니다. 전체 템플릿은 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) 에 있습니다.

## Q1. 미션

한 줄. 루프가 추구할 단일 목표.

## Q2. 운영 모드

- `continuous` — 멈추라 할 때까지
- `bounded:N` — 최대 N 사이클
- `monitor` — 외부 이벤트에만 반응

## Q3. 허용 경로 (Allow paths)

루프가 수정 가능한 글로브 패턴. 명시되지 않은 경로는 read-only.

## Q4. 금지 구역 (절대)

절대 건드릴 수 없는 브랜치/파일/플래그. 기본 차단 목록:

- `main`, `master`, `release/*`
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/`
- 허용 경로 밖에서 `--force`, `--no-verify`, `git reset --hard`, `rm -rf`
- `gh`, `npm` 외 외부 API 쓰기

## Q5. 위험 허용도 (Risk tier)

- **L1** — 발굴 + 제안만
- **L2** — 작은 PR (≤300 lines, ≤10 files) — *기본값*
- **L3** — 통과 시 자동 머지
- **L4** — 자유 모드 (Q4 금지구역은 그래도 절대)

## Q6. 주기 (Cadence)

[주기 메뉴](cadence.html) 참조.

## Q7. Escalation 트리거

기본 임계값: 연속 실패 3회, diff cap 초과, 비가역 작업, 후보 없음 시 동작 (`end` / `ask`).

## Q8. 자동 컴팩션 (Auto-compaction)

임계값(60/70/80/90, 기본 80)과 빈도(`every-cycle`, `threshold-only`, `off`).

## Q9. 업데이트 정책 (Update policy)

스킬은 `PresentJay/autopilot-skills` 의 GitHub releases 를 주기적으로 확인합니다.

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — 기본 `every-24h`
- **on_update_available**:
  - `notify` — 사이클 출력 끝에 한 줄 알림
  - `prompt` *(기본)* — 알림 + "지금 갱신할까요?" 확인. yes 시 `npx skills update PresentJay/autopilot-skills --yes` 실행
  - `silent-auto` — 묻지 않고 자동 실행

체크는 fail-open: GitHub API 오류 또는 5초 타임아웃 시 조용히 skip 하고 다음 주기에 재시도. 사이클을 절대 막지 않음.

## Q10. 재개 정책 (Resume policy)

호스트 sleep, 세션 크래시, ScheduleWakeup 누락, cycle 중단 등 인터럽트로부터 어떻게 복구할지 제어.

- **stale_threshold**: `2x-cadence` *(기본)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` 이후 얼마나 지나면 stalled 로 판정할지
- **on_resume**:
  - `auto-resume` *(기본)* — stale 감지 시 조용히 새 사이클 실행
  - `prompt-confirm` — 진단 표시("N 사이클 missed. 재개?") + 확인 후 진행
  - `manual-only` — `/autopilot resume` 또는 `/autopilot heal` 명시 신호에만 재개

Phase 0.5 가 5가지 패턴을 감지: crashed mid-cycle, missed wakeups, schedule lost, paused, escalated.

사용자 신호: `/autopilot resume`, `/autopilot heal`, `/autopilot status`.
