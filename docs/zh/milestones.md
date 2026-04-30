---
title: 里程碑
---

# 里程碑

某轮循环命中四个触发条件之一时,日志条目同时也写到 `.autopilot.milestones/<date>-<slug>.md`。这个目录是固定的 — `mission.md` 改不了它。

## 触发条件

1. **PR 合并** — 被追踪的 PR 转成 `MERGED`。
2. **Bounded 任务完成** — Q2=bounded N 达成,全部 green。
3. **首次 zero-defect** — 被追踪的缺陷类别(lint、test、type、coverage)第一次归零。通过 `state.json.defect_baselines.<category>.ever_zero` 跟踪。
4. **新出现的 NOT-OK 模式** — `mission.md` 里第一次添加的反模式。

## 为什么固定

里程碑是"什么是关键时刻"挑出来的轨迹。如果让 `mission.md` 改路径,用户就能藏掉历史 — 不可变性是为了保护审计日志。
