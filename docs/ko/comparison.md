---
layout: page
title: "비교 — autopilot vs 다른 도구"
lang: ko
---

# 다른 도구들 사이에서 autopilot의 자리

이미 ralph-loop(루프 프리미티브), impeccable(단일 스킬 OSS 패턴), 또는 gstack(개발 워크플로우 스위스 아미)을 쓰고 있을 수 있습니다. 이 페이지는 솔직합니다 — autopilot이 무엇을 더하고, 무엇이 겹치고, **언제 쓰지 말아야 하는지**.

## 한눈에

| 도구 | 핵심 목적 | 부팅 | 도메인 | 후보 자동 발굴? | 자가복구? |
|---|---|---|---|---|---|
| **autopilot** | 여러 도메인 자율주행 미션 | 슬래시 한 번 | 무엇이든 | ✅ 미션 도구로 | ✅ Phase 0.5 |
| **ralph-loop** | 일반 루프 프리미티브 (프롬프트 N회 반복) | 슬래시 한 번 | 무엇이든 | ❌ 매번 직접 입력 | ❌ |
| **impeccable** | 프론트엔드 디자인 감사 + 수정 | 슬래시 한 번 | UI / 디자인 | ✅ 디자인 도메인 한정 | ❌ |
| **gstack** | CLI 모음 (browse, ship, qa, retro, …) | 설치 + 명령 N개 | 개발 워크플로우 | 명령마다 부분적 | n/a |

## 어느 걸 언제

- **한 줄로 정리되는 도메인을 자기 알아서 돌리는 루프가 필요해** → `autopilot`
- **그냥 한 프롬프트를 N번 반복하면 돼, 거버넌스 필요 없음** → `ralph-loop`
- **프론트엔드 / 랜딩 / UX 다듬기** → `impeccable` (또는 `mission="design polish"`로 autopilot도 가능, 하지만 impeccable이 목적-제작)
- **개발 단축키 모음 (browse, qa, ship, retro)** → `gstack`

서로 **배타적이지 않습니다**. autopilot이 impeccable 사이클을 돌릴 수도, gstack을 미션 안에서 호출할 수도, ralph-loop은 autopilot이 과한 단순 루프 케이스를 커버합니다.

## ralph-loop 대비 autopilot이 더하는 것

- **미션별 거버넌스**: 허용 경로, 금지 영역, 위험 등급, diff 캡 — 모든 phase에서 강제
- **자기 페이싱**: 다음 깨우기를 cadence + idle backoff로 알아서 결정. `--max-iterations` 같은 거 불필요
- **자가복구**: 사이클 도중 크래시, 깨우기 누락, 스케줄 분실 자동 감지/복구 (Phase 0.5)
- **마일스톤 흔적**: 중요한 순간을 변경불가 디렉터리로 자동 승격
- **업데이트 알림**: 24h 캐시된 최신 릴리스 체크 + 옵트인 자동 업데이트

ralph-loop은 프리미티브, autopilot은 그 위에 직접 만들지 않아도 되도록 모양을 잡아둔 추상.

## autopilot이 **아닌** 것

- **코딩 에이전트가 아닙니다** — 이미 쓰고 있는 에이전트(Claude Code / Codex / Cursor / Gemini)를 오케스트레이트할 뿐. 자체 모델 없음.
- **CI 대체가 아닙니다** — autopilot은 commit을 쓰는 거지 파이프라인이 아님. 테스트는 여전히 CI가 돕니다.
- **코드 스타일에 의견 없음** — `mission.md`만 읽음. 스타일은 레포 + 에이전트가 이미 강제하는 그대로.
- **분산 오케스트레이터 아님** — 디렉터리당 단일 미션. 멀티 레포 팬아웃은 cron + `/schedule`로.

## 쓰지 **말아야** 하는 경우

- **일회성 작업** — 오버헤드 비효율. 그냥 에이전트한테 직접.
- **하드 리얼타임 / 프로덕션 크리티컬 쓰기** — 기본이 L2 (작은 PR, main 절대 X). 프로덕션 운용은 전용 runbook.
- **한 문장으로 안 적히는 미션** — Q1을 못 채우면 미션이 익지 않은 상태. 먼저 brainstorm, 그 다음 autopilot.
- **에이전트를 루프에 맡길 신뢰가 아직 없음** — autopilot은 에이전트의 판단을 그대로 상속. 10 사이클 신뢰 안 되면 L1(read-only)부터.

## 60초 적합도 자가진단

1. 미션을 한 문장으로 쓸 수 있는가?
2. 허용 경로의 glob이 PR 단위 사람 승인 없이 에이전트가 수정해도 괜찮은 범위인가?
3. verify 커맨드가 CI가 이미 돌리는 것인가 (build / test / lint)?

세 개 다 yes → autopilot이 맞는 모양.
