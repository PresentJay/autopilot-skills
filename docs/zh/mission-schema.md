---
title: 任务结构
---

# 任务结构

每一节就是启动问答里的一道题。完整模板在 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md)。

## Q1. 任务

一行字。这一轮循环要追的目标。

## Q2. 运行模式

- `continuous` — 直到被叫停
- `bounded:N` — 最多 N 轮
- `monitor` — 只对外部事件做反应

## Q3. 允许路径

代理能改的 glob 模式。没列出来的,只读。

## Q4. 禁区

任何情况下都不碰的分支、文件、参数。默认拦截:

- `main`、`master`、`release/*`
- `.env`、`*credentials*`、`secrets/*`、`*.pem`、`*.key`
- `infra/`、`terraform/`、`.github/workflows/`
- 允许路径以外的 `--force`、`--no-verify`、`git reset --hard`、`rm -rf`
- 除了 `gh` 和 `npm` 之外的外部 API 写入

## Q5. 风险等级

- **L1** — 只发现 + 提议
  - 什么时候? 只想拿建议时。新仓库第一次跑,合规环境,只做 audit。
- **L2** — 小的 PR (≤300 行,≤10 文件) — *默认*
  - 什么时候? 大多数情况。人能评审的小 diff,CI 把关。
- **L3** — 通过就自动合并
  - 什么时候? CI 可靠、允许 bot PR 自动合并的仓库。
- **L4** — 自由模式(Q4 禁区还是绝对的)
  - 什么时候? 跟你商量好的大重构、多 PR 实验。Q4 还是挡住所有破坏性操作。

## Q6. 节奏

参见[节奏菜单](cadence.html)。

## Q7. 升级触发条件

什么时候循环应该停下来通知你,而不是硬继续往下跑。

- **连续失败 3 次** — 同一候选 3 轮失败 → 加进 NOT-OK 然后跳过。所有候选都失败时,escalate。
- **超出 diff cap** — 提议的改动比该 tier 允许的还大 → 先拆成子任务,还是超就 escalate。
- **不可逆操作** — 数据库 DDL、force-push、外部 API 写入 — 执行前必须 escalate。
- **没有候选**:
  - `end` *(默认)* — 当作任务完成,不再 ScheduleWakeup。
  - `ask` — 向你要更多的发现工具。
- **允许路径外候选 ≥5 个** — 提议扩展任务范围。

## Q8. 自动压缩

长任务跑久了会撞 prompt-too-long,所以定期把对话裁掉。`/compact` 会把旧记录清掉、保留最近状态。

- **threshold** — 令牌使用率超过这个百分比就 pause-and-compact。
  - 什么时候? 令牌重的活(大 diff、大文件)选 60-70;一般文档/代码循环选 80-90。默认 **80**。
- **frequency**:
  - `every-cycle` *(默认)* — 每轮做一次轻量压缩。成本可预测,长会话最安全。
  - `threshold-only` — 只在超阈值时压缩。短会话省令牌。
  - `off` — 不压缩。仅适合短的 bounded 任务,或你自己管上下文。

## Q9. 更新策略

技能会定期看一眼 GitHub releases 有没有新版。

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — 默认 `every-24h`
  - 什么时候? 每天都在用的仓库选 `every-24h`;想第一时间拿到新版选 `every-boot`;发布慢的项目选 `weekly`;打算手动更新选 `off`。
- **on_update_available**:
  - `notify` — 在循环输出末尾加一行通知。*什么时候?* 每轮输出本来就会看。
  - `prompt` *(默认)* — 提示一下,问"现在更新吗?",同意就跑 `npx skills update PresentJay/autopilot-skills --yes`。*什么时候?* 偶尔看一眼、想要明确同意。
  - `silent-auto` — 不问,直接跑。*什么时候?* 信任的环境,不会逐条看日志。

检查是 fail-open: GitHub API 报错或 5 秒超时就静默跳过,下次再试。绝对不会卡住循环。

## Q10. 恢复策略

主机 sleep、会话崩了、ScheduleWakeup 没触发、循环中断 —— 控制怎么恢复。

- **stale_threshold**: `2x-cadence` *(默认)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` 之后过多久判定 stalled。
  - 什么时候? 想激进恢复(1 轮丢失就算 stalled)选 `2x-cadence`;基础设施稳定但偶尔负载选 `4x-cadence`;周期长、主机夜间 sleep 很常见选 `8x-cadence`。
- **on_resume**:
  - `auto-resume` *(默认)* — 看到 stale 就静默跑新一轮。*什么时候?* 信任循环、不想打断节奏。
  - `prompt-confirm` — 显示诊断("Missed N cycles. Resume?"),确认后再继续。*什么时候?* 想知道每一次恢复。
  - `manual-only` — 只在 `/autopilot resume` 或 `/autopilot heal` 这种明确信号下才恢复。*什么时候?* 任务是有意 pause 的,自己再决定什么时候继续。

Phase 0.5 检测五种情况: crashed mid-cycle、missed wakeups、schedule lost、paused、escalated。

用户信号: `/autopilot resume`、`/autopilot heal`、`/autopilot status`。
