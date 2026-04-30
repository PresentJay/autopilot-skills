---
title: 미션 스키마
---

# 미션 스키마

각 섹션은 부트업 인터뷰의 한 문항입니다. 전체 템플릿은 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) 에 있습니다.

## Q1. 미션

한 줄. 루프가 추구할 단일 목표입니다.

## Q2. 운영 모드

- `continuous` — 멈추라 할 때까지 계속
- `bounded:N` — 최대 N 사이클
- `monitor` — 외부 이벤트에만 반응

## Q3. 허용 경로

루프가 수정할 수 있는 글로브 패턴. 명시되지 않은 경로는 read-only 입니다.

## Q4. 금지 구역

절대 건드리지 않는 브랜치 · 파일 · 플래그. 기본 차단 목록:

- `main`, `master`, `release/*`
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/`
- 허용 경로 밖에서의 `--force`, `--no-verify`, `git reset --hard`, `rm -rf`
- `gh`, `npm` 외 외부 API 쓰기

## Q5. 위험 허용도

- **L1** — 발굴과 제안만
- **L2** — 작은 PR (≤300 lines, ≤10 files) — *기본값*
- **L3** — 통과 시 자동 머지
- **L4** — 자유 모드 (그래도 Q4 금지구역은 절대)

## Q6. 주기

[주기 메뉴](cadence.html) 참조.

## Q7. Escalation 트리거

기본 임계값: 연속 실패 3회, diff cap 초과, 비가역 작업, 후보 없음 시 동작 (`end` / `ask`).

## Q8. 자동 컴팩션

임계값(60 / 70 / 80 / 90, 기본 80)과 빈도(`every-cycle`, `threshold-only`, `off`).

## Q9. 업데이트 정책

스킬은 GitHub releases 에서 새 버전을 주기적으로 확인합니다.

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — 기본 `every-24h`
- **on_update_available**:
  - `notify` — 사이클 출력 끝에 한 줄 알림
  - `prompt` *(기본)* — 알림 + "지금 갱신할까요?" 확인. 동의 시 `npx skills update PresentJay/autopilot-skills --yes` 실행
  - `silent-auto` — 묻지 않고 자동 실행

체크는 fail-open: GitHub API 오류나 5초 타임아웃 시 조용히 건너뛰고 다음 주기에 다시 시도합니다. 사이클을 절대 막지 않습니다.

## Q10. 재개 정책

호스트 sleep, 세션 크래시, ScheduleWakeup 누락, 사이클 중단 등 인터럽트로부터 어떻게 복구할지 결정합니다.

- **stale_threshold**: `2x-cadence` *(기본)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` 이후 얼마나 지나면 stalled 로 판정할지
- **on_resume**:
  - `auto-resume` *(기본)* — stale 감지 시 조용히 새 사이클 시작
  - `prompt-confirm` — 진단을 보여주고 ("N 사이클이 누락되었습니다. 재개?") 확인 후 진행
  - `manual-only` — `/autopilot resume` 또는 `/autopilot heal` 명시 신호에만 재개

Phase 0.5 가 다섯 패턴을 감지합니다: crashed mid-cycle, missed wakeups, schedule lost, paused, escalated.

사용자 신호: `/autopilot resume`, `/autopilot heal`, `/autopilot status`.
