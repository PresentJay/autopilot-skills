---
title: 里程碑
---

# 里程碑

当某次循环命中 4 个触发条件之一,日志条目会**额外**写入 `.autopilot.milestones/<date>-<slug>.md`。该目录是固定的 — `mission.md` 无法重定位它。

## 触发条件

1. **PR 合并** — 被追踪的 PR 转为 `MERGED` 状态。
2. **Bounded 任务完成** — Q2=bounded N 达成且全部 green。
3. **首次 zero-defect 达成** — 被追踪的缺陷类别(lint、test、type、coverage)首次归零。通过 `state.json` 的 `defect_baselines.<category>.ever_zero` 跟踪。
4. **新出现的 NOT-OK 模式** — `mission.md` 中首次添加的反模式。

## 为什么固定

里程碑是"什么是重要时刻"的精选轨迹。如果允许在 `mission.md` 中改路径,用户就能隐藏历史 — 不可变性保护审计日志。
