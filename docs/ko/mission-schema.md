---
title: 미션 스키마
---

# 미션 스키마

각 섹션은 셋업에서 답하는 한 문항입니다. 전체 템플릿은 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) 에 있어요.

## Q1. 미션

한 줄. 사이클이 좇을 단일 목표.

## Q2. 운영 모드

- `continuous` — 멈추라 할 때까지 계속.
  - 언제? 끝나는 시점이 안 보이는 품질 작업 (lint 정리, dead-code 청소, 문서 다듬기) 등.
- `bounded:N` — 최대 N 사이클.
  - 언제? 정해진 체크리스트가 있을 때 (예: 5개 작업). N 사이클 후 자동 종료.
- `monitor` — 외부 이벤트에만 반응.
  - 언제? 타이머 대신 신호 (CI 완료, 새 PR, 로그 라인) 로 깨우고 싶을 때.

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

루프가 그냥 밀고 가기보다 멈춰서 알려야 할 상황.

- **연속 실패 3회** — 같은 후보가 3 사이클 실패 → NOT-OK 에 넣고 넘어감. 모든 후보가 실패하면 escalate.
- **Diff cap 초과** — 제안 변경이 tier 한계를 넘김 → 먼저 sub-task 로 쪼개고, 그래도 넘치면 escalate.
- **비가역 작업** — DB DDL, force-push, 외부 API 쓰기 — 실행 전 무조건 escalate.
- **후보 없음**:
  - `end` *(기본)* — 미션 완료로 간주. ScheduleWakeup 안 함.
  - `ask` — 추가 발굴 도구를 사용자에게 요청.
- **허용 경로 밖 후보 5개 이상** — 미션 범위 확장 제안.

## Q8. 컴팩션 전략 (v1.3.0 개정)

장기 미션이 prompt-too-long 에 부딪히지 않도록 대화 트리밍이 필요한데, **agent 가 `/compact` 를 직접 호출할 수 없습니다** — 모든 현행 하니스(Claude Code / Codex / Cursor / Gemini)에서 사용자 입력 슬래시 명령. 스킬은 *제안*만, 실행은 사용자(또는 `/schedule` cron) 몫.

- **threshold** — 토큰 사용량이 이 비율을 넘으면 권고 메시지 출력.
  - 언제? 큰 diff/대용량 파일 작업이면 낮게(60-70), 일반 docs/코드 사이클이면 높게(80-90). 기본 **80**.
- **strategy**:
  - `auto-suggest` *(기본)* — 임계점 넘으면 `📦 /compact 권고` 한 줄 출력. 사용자가 `/compact` 입력.
  - `cron-promote` — 정말 긴 미션이면 `/schedule "<cron> /autopilot"` 추천. cron 으로 호출되는 매 사이클이 새 세션이라 컴팩션 불필요.
  - `off` — 조용히. 짧은 bounded 미션 전용.

## Q9. 업데이트 정책

GitHub releases 에서 새 버전이 나왔는지 주기적으로 확인합니다.

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — 기본 `every-24h`
  - 언제? 매일 작업하는 레포는 `every-24h`. 새 버전 빨리 받고 싶으면 `every-boot`. 릴리즈 주기 긴 도구는 `weekly`. 직접 업데이트할 거면 `off`.
- **on_update_available**:
  - `notify` — 사이클 출력 끝에 한 줄 알림. *언제?* 매 사이클 출력 어차피 읽는 경우.
  - `prompt` *(기본)* — 알림 + "지금 갱신할까요?" 물어보고, 동의 시 `npx skills update PresentJay/autopilot-skills --yes` 실행. *언제?* 가끔 보면서 동의 한 번 받고 싶을 때.
  - `silent-auto` — 묻지 않고 바로 갱신. *언제?* 신뢰하는 셋업, 로그 일일이 안 볼 때.

체크 실패는 fail-open: GitHub API 오류나 5초 타임아웃 시 조용히 건너뛰고 다음 주기에 다시 시도. 사이클을 절대 막지 않습니다.

## Q10. 재개 정책

호스트 sleep, 세션 크래시, ScheduleWakeup 누락, 사이클 중단 등으로 끊겼을 때 어떻게 다시 살릴지 결정합니다.

- **stale_threshold**: `2x-cadence` *(기본)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` 이후 얼마나 지나면 stalled 로 볼지.
  - 언제? 공격적으로 복구하려면 `2x-cadence` (1 사이클 누락 = stalled). 인프라 안정적이고 가끔 부하 있으면 `4x-cadence`. 주기 긴 미션에서 호스트 야간 sleep 자주 일어나면 `8x-cadence`.
- **on_resume**:
  - `auto-resume` *(기본)* — stale 감지 시 조용히 새 사이클 시작. *언제?* 루프 신뢰, 흐름 끊기기 싫을 때.
  - `prompt-confirm` — 진단 보여주고 ("N 사이클 누락. 재개?") 확인 후 진행. *언제?* 복구 매 건 알고 싶을 때.
  - `manual-only` — `/autopilot resume` 또는 `/autopilot heal` 신호 있을 때만 재개. *언제?* 의도적으로 pause 한 미션, 사용자가 직접 재개할 때.

Phase 0.5 가 다섯 패턴을 잡습니다: crashed mid-cycle, missed wakeups, schedule lost, paused, escalated.

사용자 신호: `/autopilot resume`, `/autopilot heal`, `/autopilot status`, `/autopilot version`.
