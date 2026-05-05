---
layout: page
title: "对比 —— autopilot 和其他工具"
lang: zh
---

# autopilot 在工具生态中的位置

你可能已经在用 ralph-loop(循环原语)、impeccable(单一技能 OSS 模板)或 gstack(开发瑞士军刀)。本页坦诚说明:autopilot 多了什么、和它们重在哪儿、**什么时候别用**。

## 一览

| 工具 | 主要目的 | 启动 | 领域 | 自动发现工作? | 自愈? |
|---|---|---|---|---|---|
| **autopilot** | 跨领域自主任务 | 一条斜杠命令 | 任意 | ✅ 通过任务工具 | ✅ Phase 0.5 |
| **ralph-loop** | 通用循环原语(把 prompt 跑 N 次) | 一条斜杠命令 | 任意 | ❌ 每次自己写 | ❌ |
| **impeccable** | 前端设计审查 + 修复 | 一条斜杠命令 | UI / 设计 | ✅ 限设计域 | ❌ |
| **gstack** | CLI 套件(browse、ship、qa、retro…) | 安装 + N 条命令 | 开发流程 | 各命令局部 | 不适用 |

## 什么时候选哪个

- **想要在一句话能描述的领域里自己跑的循环** → `autopilot`
- **就是要把一条 prompt 跑 N 次,治理无所谓** → `ralph-loop`
- **打磨前端 / 落地页 / UX** → `impeccable`(或用 `mission="design polish"` 让 autopilot 跑,但 impeccable 是专门做这个)
- **开发快捷工具集(browse、qa、ship、retro)** → `gstack`

它们 **并不互斥**。autopilot 可以驱动 impeccable 周期、gstack 可以在 autopilot 任务里调用、ralph-loop 覆盖 autopilot 显得过重的纯循环场景。

## autopilot 相对 ralph-loop 多出的部分

- **每任务治理**:允许路径、禁区、风险等级、diff 上限 —— 每个 phase 强制
- **自调速**:下一次唤醒由 cadence + 空闲退避自动决定,不需要 `--max-iterations`
- **自愈**:中途崩溃、错过唤醒、调度丢失会被检测并恢复(Phase 0.5)
- **里程碑留痕**:关键时刻自动晋升到不可变目录
- **更新提醒**:24h 缓存检查最新发布版本 + 可选自动更新

ralph-loop 是原语,autopilot 是在它之上不必你手搓的形状。

## autopilot **不是**

- **不是编程代理** —— 它编排的是你已经在用的代理(Claude Code / Codex / Cursor / Gemini)。本身不带模型。
- **不是 CI 替代** —— autopilot 写的是 commit,不是流水线。测试还是 CI 跑。
- **对代码风格没有意见** —— 只读 `mission.md`。风格仍由仓库和底层代理执行。
- **不是分布式调度器** —— 一个目录一个任务。跨仓库分发请用 cron + `/schedule`。

## 什么时候 **别** 用

- **一次性任务** —— 开销不划算。直接问代理就行。
- **硬实时 / 生产关键写入** —— autopilot 默认 L2(小 PR、绝不直推 main)。生产操作请用专门 runbook。
- **任务无法用一句话写出来** —— Q1 写不出来就是没成熟。先 brainstorm,再 autopilot。
- **还不放心把代理交给循环** —— autopilot 直接继承代理的判断。如果 10 个周期都不放心,从 L1(只读提案)起步。

## 60 秒适配自检

1. 能用一句话写出任务吗?
2. 允许路径的 glob 是否在你愿意让代理改动而不必每个 PR 人工审核的范围内?
3. verify 命令是不是 CI 已经在跑的(build / test / lint)?

三个都 yes → autopilot 就是对的形状。
