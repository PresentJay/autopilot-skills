---
title: 任务结构
---

# 任务结构

每一节对应启动问答中的一道题。完整模板见 [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md)。

## Q1. 任务

一行文字。循环要追求的单一目标。

## Q2. 运行模式

- `continuous` — 直到被叫停
- `bounded:N` — 最多 N 个循环
- `monitor` — 仅响应外部事件

## Q3. 允许路径

循环可修改的 glob 模式。未列出的路径为只读。

## Q4. 禁区(绝对)

任何情况都不会触碰的分支/文件/标志。默认拦截:

- `main`, `master`, `release/*`
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/`
- 在允许路径外的 `--force`、`--no-verify`、`git reset --hard`、`rm -rf`
- 除 `gh` 与 `npm` 之外的外部 API 写入

## Q5. 风险等级

- **L1** — 仅发现 + 提议
- **L2** — 小型 PR (≤300 行,≤10 文件) — *默认*
- **L3** — 通过后自动合并
- **L4** — 自由模式 (Q4 禁区仍然绝对)

## Q6. 节奏

参见[节奏菜单](cadence.html)。

## Q7. 升级触发条件

默认阈值: 连续失败 3 次、超出 diff cap、不可逆操作、无候选时行为 (`end` / `ask`)。

## Q8. 自动压缩 (Auto-compaction)

阈值(60/70/80/90,默认 80)和频率(`every-cycle`、`threshold-only`、`off`)。
