---
title: 시작하기
---

# 시작하기

## 설치

```bash
npx skills add PresentJay/autopilot-skills
```

프롬프트에서 사용 중인 하니스를 선택하거나, 모든 하니스에 한 번에 깔려면 `--all -g` 를 추가하세요.

## 미션 시작

하니스(Claude Code · Codex · Cursor 등)에서:

```
/autopilot
```

처음 호출하면 10문항 인터뷰가 시작됩니다. 이미 결정한 답이 있으면 인자로 넘겨 인터뷰를 건너뛸 수 있습니다.

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## 멈추기

- "stop autopilot" / "멈춰" / "pause" — `mission.md` 의 Mode 가 `paused` 로 바뀝니다.
- `.autopilot.log/mission.md` 를 삭제 — 다음 호출 시 cold start.
