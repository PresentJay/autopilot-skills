---
title: 安全策略
---

# 安全策略

不只是 EXECUTE 阶段,**每一个阶段**都在跑这套规则。

## 禁区

任务的 Q4。一旦碰上,当场 abort,写进日志。哪怕风险等级是 L4,Q4 也不退让。

## 预执行黑名单

下面这些命令在 pre-execute 阶段就被挡掉:

- `git push --force`
- `git reset --hard`
- `rm -rf <允许路径外>`
- 数据库 DDL
- 外部 API 写入

只有 `mission.md` 里显式打开 opt-in,才会放行。

## NOT-OK 模式自动累积

失败的提议会进 `mission.md` 的 `NOT-OK patterns`。下一轮就避开这个坑。

## 空闲上限

连续 3 个空循环就把节奏 +1 档,累计 10 个空循环就提议终止。

## 令牌预算

单轮用量到 70%,触发 split-cycle 保存,而不是直接判失败。
