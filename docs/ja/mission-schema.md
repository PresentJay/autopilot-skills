---
title: ミッションスキーマ
---

# ミッションスキーマ

各セクションは起動インタビューの 1 問です。完全なテンプレートは [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) にあります。

## Q1. ミッション

一行。ループが追求する単一の目標。

## Q2. 動作モード

- `continuous` — 停止指示まで継続
- `bounded:N` — 最大 N サイクル
- `monitor` — 外部イベントにのみ反応

## Q3. 許可パス

ループが変更可能な glob パターン。リストにないパスは read-only。

## Q4. 禁止ゾーン

何があっても触らないブランチ・ファイル・フラグ。デフォルトのブロックリスト:

- `main`・`master`・`release/*`
- `.env`・`*credentials*`・`secrets/*`・`*.pem`・`*.key`
- `infra/`・`terraform/`・`.github/workflows/`
- 許可パス外での `--force`・`--no-verify`・`git reset --hard`・`rm -rf`
- `gh` と `npm` 以外の外部 API への書き込み

## Q5. リスク階層

- **L1** — 発見と提案のみ
- **L2** — 小さな PR (≤300 行、≤10 ファイル) — *デフォルト*
- **L3** — グリーンになり次第マージ
- **L4** — 自由モード(Q4 禁止ゾーンは依然として絶対)

## Q6. サイクル

[サイクルメニュー](cadence.html)を参照。

## Q7. エスカレーション トリガー

デフォルトの閾値: 連続失敗 3 回、diff cap 超過、不可逆操作、候補なし時の動作 (`end` / `ask`)。

## Q8. 自動コンパクション

閾値(60 / 70 / 80 / 90、デフォルト 80)と頻度 (`every-cycle`・`threshold-only`・`off`)。

## Q9. アップデートポリシー

スキルは GitHub releases を定期的にチェックします。

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — デフォルト `every-24h`
- **on_update_available**:
  - `notify` — サイクル出力の末尾に 1 行の通知を追加
  - `prompt` *(デフォルト)* — 通知 + 「今すぐアップデート?」を確認。承認後 `npx skills update PresentJay/autopilot-skills --yes` を実行
  - `silent-auto` — 確認なしで自動実行

チェックは fail-open: GitHub API エラーまたは 5 秒タイムアウトの場合は静かにスキップし、次回リトライ。サイクルを絶対にブロックしません。

## Q10. 再開ポリシー

中断(ホスト sleep、セッションクラッシュ、ScheduleWakeup の取りこぼし、サイクル中断)からどう復旧するかを制御します。

- **stale_threshold**: `2x-cadence` *(デフォルト)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` からどれだけ経過したら stalled と判定するか
- **on_resume**:
  - `auto-resume` *(デフォルト)* — stale 検出時、静かに新サイクルを実行
  - `prompt-confirm` — 診断(「N サイクルが取りこぼされました。再開?」)を表示し、確認後に続行
  - `manual-only` — `/autopilot resume` または `/autopilot heal` の明示シグナル時のみ復旧

Phase 0.5 が 5 つのパターンを検出します: crashed mid-cycle、missed wakeups、schedule lost、paused、escalated。

ユーザーシグナル: `/autopilot resume`、`/autopilot heal`、`/autopilot status`。
