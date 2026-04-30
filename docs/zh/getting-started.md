---
title: 入门
---

# 入门

## 安装

```bash
npx skills add PresentJay/autopilot-skills
```

按提示选你正在用的代理,或者加 `--all -g` 一次性全装。

## 启动任务

在你用的代理(Claude Code、Codex、Cursor 等)里:

```
/autopilot
```

第一次跑会进 10 题问答。已经决定的答案可以直接传参跳过。

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## 停下

- "stop autopilot" / "멈춰" / "pause" — `mission.md` 的 Mode 变成 `paused`。
- 删掉 `.autopilot.log/mission.md` — 下次调用从头来。
