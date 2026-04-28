---
title: 安全策略
---

# 安全策略

不只是 EXECUTE 阶段,**每一个阶段**都强制执行。

## 禁区

任务的 Q4。一旦匹配 → 立即 abort + 写入日志。即使风险等级为 L4,Q4 仍然绝对。

## 预执行黑名单 (pre-execute deny-list)

- `git push --force`
- `git reset --hard`
- `rm -rf <允许路径外>`
- 数据库 DDL
- 外部 API 写入

仅在 `mission.md` 显式 opt-in 时才允许。

## NOT-OK 模式自动累积

失败的提议会被加入 `mission.md` 的 `NOT-OK patterns`。后续循环避开同一陷阱。

## 空闲上限

连续 3 个空循环 → 节奏 +1 档。累计 10 个空循环 → 提议终止。

## 令牌预算

单个循环达到 70% 上限时,触发 split-cycle 保存(而非视为失败)。
