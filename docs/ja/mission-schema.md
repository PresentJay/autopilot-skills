---
title: ミッションスキーマ
---

# ミッションスキーマ

各セクションは起動インタビューの 1 問です。完全なテンプレートは [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) にあります。

## Q1. ミッション

1 行。ループが追求する単一の目標。

## Q2. 動作モード

- `continuous` — 停止指示まで継続
- `bounded:N` — 最大 N サイクル
- `monitor` — 外部イベントにのみ反応

## Q3. 許可パス (Allow paths)

ループが変更可能な glob パターン。リストにないパスは read-only。

## Q4. 禁止ゾーン(絶対)

何があっても触らないブランチ/ファイル/フラグ。デフォルトのブロックリスト:

- `main`, `master`, `release/*`
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/`
- 許可パス外での `--force`、`--no-verify`、`git reset --hard`、`rm -rf`
- `gh` と `npm` 以外の外部 API への書き込み

## Q5. リスク階層 (Risk tier)

- **L1** — 発見 + 提案のみ
- **L2** — 小さな PR (≤300 lines, ≤10 files) — *デフォルト*
- **L3** — グリーンになり次第マージ
- **L4** — 自由モード (Q4 禁止ゾーンは依然として絶対)

## Q6. サイクル (Cadence)

[サイクルメニュー](cadence.html)を参照。

## Q7. エスカレーション トリガー

デフォルトの閾値: 連続失敗 3 回、diff cap 超過、不可逆操作、候補なし時の動作 (`end` / `ask`)。

## Q8. 自動コンパクション (Auto-compaction)

閾値(60/70/80/90、デフォルト 80)と頻度(`every-cycle`、`threshold-only`、`off`)。
