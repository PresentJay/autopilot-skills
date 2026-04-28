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
