---
title: 시작하기
---

# 시작하기

## 설치

```bash
npx skills add PresentJay/autopilot-skills
```

쓰는 도구를 프롬프트에서 고르거나, `--all -g` 로 한 번에 다 깔 수 있어요.

## 미션 시작

도구(Claude Code · Codex · Cursor 등)에서:

```
/autopilot
```

처음 호출하면 10 문항 셋업이 뜹니다. 이미 정해 둔 답이 있으면 인자로 같이 넘겨 인터뷰를 건너뛸 수 있어요.

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## 멈추기

- "stop autopilot" / "멈춰" / "pause" — `mission.md` Mode 가 `paused` 로 바뀝니다.
- `.autopilot.log/mission.md` 삭제 — 다음 호출 때 처음부터 다시.
