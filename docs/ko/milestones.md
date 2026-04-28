---
title: 마일스톤
---

# 마일스톤

사이클이 4가지 트리거 중 하나에 매칭되면, 저널 항목이 **추가로** `.autopilot.milestones/<date>-<slug>.md` 에 기록됩니다. 이 폴더는 고정 — `mission.md` 로 경로를 바꿀 수 없습니다.

## 트리거

1. **PR merged** — 추적 중인 PR 이 `MERGED` 로 전환된 사이클.
2. **Bounded 미션 완료** — Q2=bounded N 도달 + 모두 green.
3. **첫 zero-defect 달성** — 추적 중인 결함 카테고리(lint, test, type, coverage)가 처음으로 0 도달. `state.json` 의 `defect_baselines.<category>.ever_zero` 로 추적.
4. **신규 NOT-OK 패턴** — `mission.md` 에 처음 추가된 안티패턴.

## 왜 고정인가

마일스톤은 "무엇이 중요했는지" 의 큐레이트된 흔적입니다. `mission.md` 에서 경로 변경을 허용하면 사용자가 역사를 숨길 수 있어 — 불변성이 audit log 를 보호합니다.
