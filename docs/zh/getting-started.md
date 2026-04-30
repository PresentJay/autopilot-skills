---
title: 入门
---

# 入门

## 安装

```bash
npx skills add PresentJay/autopilot-skills
```

按提示选择代理,或加 `--all -g` 一次性全部安装。

## 启动任务

在你使用的代理(Claude Code、Codex、Cursor 等)中:

```
/autopilot
```

首次调用会进入 10 题问答。已经决定的答案可以通过参数传入,跳过对应问题。

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## 停止

- "stop autopilot" / "멈춰" / "pause" — 将 `mission.md` 的 Mode 设为 `paused`。
- 删除 `.autopilot.log/mission.md` — 下次调用从冷启动开始。
