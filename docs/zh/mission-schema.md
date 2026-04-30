---
title: 任务结构
---

# 任务结构

每一节对应启动问答中的一道题。完整模板见 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md)。

## Q1. 任务

一行字。循环要追求的单一目标。

## Q2. 运行模式

- `continuous` — 直到被叫停
- `bounded:N` — 最多 N 个循环
- `monitor` — 仅响应外部事件

## Q3. 允许路径

循环可以修改的 glob 模式。未列出的路径为只读。

## Q4. 禁区

任何情况下都不会触碰的分支、文件、标志。默认拦截:

- `main`、`master`、`release/*`
- `.env`、`*credentials*`、`secrets/*`、`*.pem`、`*.key`
- `infra/`、`terraform/`、`.github/workflows/`
- 允许路径外的 `--force`、`--no-verify`、`git reset --hard`、`rm -rf`
- 除 `gh` 与 `npm` 之外的外部 API 写入

## Q5. 风险等级

- **L1** — 仅发现与提议
- **L2** — 小型 PR (≤300 行,≤10 文件) — *默认*
- **L3** — 通过后自动合并
- **L4** — 自由模式(Q4 禁区仍然绝对)

## Q6. 节奏

参见[节奏菜单](cadence.html)。

## Q7. 升级触发条件

默认阈值:连续失败 3 次、超出 diff cap、不可逆操作、无候选时行为(`end` / `ask`)。

## Q8. 自动压缩

阈值(60 / 70 / 80 / 90,默认 80)与频率(`every-cycle`、`threshold-only`、`off`)。

## Q9. 更新策略

技能会定期向 GitHub releases 检查新版本。

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — 默认 `every-24h`
- **on_update_available**:
  - `notify` — 在循环输出末尾追加一行通知
  - `prompt` *(默认)* — 通知 + "立即更新?" 确认。同意后执行 `npx skills update PresentJay/autopilot-skills --yes`
  - `silent-auto` — 不询问,自动执行

检查 fail-open: GitHub API 报错或 5 秒超时时静默跳过,下次再试。绝不阻塞循环。

## Q10. 恢复策略

控制技能如何从中断(主机 sleep、会话崩溃、ScheduleWakeup 丢失、循环中断)中恢复。

- **stale_threshold**: `2x-cadence` *(默认)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` 之后多久判定为 stalled
- **on_resume**:
  - `auto-resume` *(默认)* — 检测到 stale 时静默运行新循环
  - `prompt-confirm` — 显示诊断("Missed N cycles. Resume?")并确认后继续
  - `manual-only` — 仅在显式信号 `/autopilot resume` 或 `/autopilot heal` 时恢复

Phase 0.5 检测五种模式: crashed mid-cycle、missed wakeups、schedule lost、paused、escalated。

用户信号: `/autopilot resume`、`/autopilot heal`、`/autopilot status`。
