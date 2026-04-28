---
title: 안전 정책
---

# 안전 정책

EXECUTE 단계뿐 아니라 **모든 단계**에서 강제됩니다.

## 금지 구역

미션의 Q4. 매칭되면 → 즉시 abort + 저널 기록. 위험 허용도 L4 라도 Q4는 절대.

## 사전 차단 목록 (pre-execute deny-list)

- `git push --force`
- `git reset --hard`
- `rm -rf <허용 경로 밖>`
- DB DDL
- 외부 API 쓰기

`mission.md` 가 명시적으로 opt-in 한 경우에만 허용.

## NOT-OK 패턴 자동 누적

실패한 후보는 `mission.md` 의 `NOT-OK patterns` 에 추가됩니다. 이후 사이클은 같은 함정을 회피합니다.

## 유휴 한도

연속 3 사이클이 비면 → 주기 1단계 증가. 누적 10 사이클이 비면 → 종료 제안.

## 토큰 예산

사이클당 70% 한도 초과 시 split-cycle 저장 모드로 전환 (실패 처리 X).
