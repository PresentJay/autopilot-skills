---
title: 미션 스키마
---

# 미션 스키마

각 섹션은 셋업에서 답하는 한 문항입니다. 전체 템플릿은 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) 에 있어요.

## Q1. 미션

한 줄. 사이클이 좇을 단일 목표.

## Q2. 운영 모드

- `continuous` — 멈추라 할 때까지 계속
- `bounded:N` — 최대 N 사이클
- `monitor` — 외부 이벤트에만 반응

## Q3. 허용 경로

사이클이 손댈 수 있는 글로브 패턴. 명시 안 된 경로는 read-only.

## Q4. 금지 구역

절대 건드리지 않음. 기본 차단 목록:

- `main`, `master`, `release/*`
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/`
- 허용 경로 밖에서의 `--force`, `--no-verify`, `git reset --hard`, `rm -rf`
- `gh`, `npm` 외 외부 API 쓰기

## Q5. 위험 허용도

- **L1** — 발굴과 제안만
  - 언제? 검토 의견만 받고 싶을 때. 신규 레포 첫 미션, 규제 환경, audit-only.
- **L2** — 작은 PR (≤300 lines, ≤10 files) — *기본*
  - 언제? 대부분의 경우. 사람이 리뷰할 수 있는 작은 diff, CI 게이트.
- **L3** — 통과 시 자동 머지
  - 언제? CI 신뢰도 높고 봇 PR 자동 머지가 허용되는 레포.
- **L4** — 자유 모드 (그래도 Q4 는 절대)
  - 언제? 사용자와 합의된 대형 리팩터, 멀티 PR 실험. Q4 차단은 그대로.

## Q6. 주기

[주기 메뉴](cadence.html) 참조.

## Q7. Escalation 트리거

기본: 연속 실패 3회, diff cap 초과, 비가역 작업, 후보 없음 시 동작 (`end` / `ask`).

## Q8. 자동 컴팩션

임계값(60 / 70 / 80 / 90, 기본 80) · 빈도(`every-cycle`, `threshold-only`, `off`).

## Q9. 업데이트 정책

GitHub releases 에서 새 버전이 나왔는지 주기적으로 확인합니다.

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — 기본 `every-24h`
- **on_update_available**:
  - `notify` — 사이클 출력 끝에 한 줄 알림
  - `prompt` *(기본)* — 알림 + "지금 갱신할까요?" 물어보고, 동의 시 `npx skills update PresentJay/autopilot-skills --yes` 실행
  - `silent-auto` — 묻지 않고 바로 갱신

체크 실패는 fail-open: GitHub API 오류나 5초 타임아웃 시 조용히 건너뛰고 다음 주기에 다시 시도. 사이클을 절대 막지 않습니다.

## Q10. 재개 정책

호스트 sleep, 세션 크래시, ScheduleWakeup 누락, 사이클 중단 등으로 끊겼을 때 어떻게 다시 살릴지 결정합니다.

- **stale_threshold**: `2x-cadence` *(기본)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` 이후 얼마나 지나면 stalled 로 볼지
- **on_resume**:
  - `auto-resume` *(기본)* — stale 감지 시 조용히 새 사이클 시작
  - `prompt-confirm` — 진단 보여주고 ("N 사이클 누락. 재개?") 확인 후 진행
  - `manual-only` — `/autopilot resume` 또는 `/autopilot heal` 신호 있을 때만 재개

Phase 0.5 가 다섯 패턴을 잡습니다: crashed mid-cycle, missed wakeups, schedule lost, paused, escalated.

사용자 신호: `/autopilot resume`, `/autopilot heal`, `/autopilot status`.
