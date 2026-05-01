---
title: ミッションスキーマ
---

# ミッションスキーマ

各セクションがセットアップで答える 1 問にあたります。完全なテンプレートは [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md) にあります。

## Q1. ミッション

一行。サイクルが追いかける単一の目標。

## Q2. 動作モード

- `continuous` — 止めるまで続ける。
  - いつ? 終わりが読めない品質改善(lint クリーンアップ、デッドコード整理、ドキュメント磨き込み)など。
- `bounded:N` — 最大 N サイクル。
  - いつ? 決まったチェックリストがあるとき(例: 5 タスク)。N サイクル後に自動終了。
- `monitor` — 外部イベントにだけ反応する。
  - いつ? タイマーではなくシグナル(CI 完了、新 PR、ログ行)で起こしたいとき。

## Q3. 許可パス

サイクルが触れる glob パターン。リストにないものは read-only。

## Q4. 禁止ゾーン

何があっても触らないブランチ・ファイル・フラグ。デフォルトのブロックリスト:

- `main`・`master`・`release/*`
- `.env`・`*credentials*`・`secrets/*`・`*.pem`・`*.key`
- `infra/`・`terraform/`・`.github/workflows/`
- 許可パス外での `--force`・`--no-verify`・`git reset --hard`・`rm -rf`
- `gh` と `npm` 以外の外部 API への書き込み

## Q5. リスク階層

- **L1** — 発見と提案だけ
  - いつ? 提案だけ欲しいとき。初めてのリポジトリ、規制下、audit 専用。
- **L2** — 小さな PR (≤300 行・≤10 ファイル) — *デフォルト*
  - いつ? たいていのケース。人がレビューできる差分、CI ゲート。
- **L3** — 通ったら自動マージ
  - いつ? CI の信頼性が高く、bot PR の自動マージを許す環境。
- **L4** — 自由モード(Q4 禁止ゾーンは依然として絶対)
  - いつ? ユーザーと合意した大規模リファクタ、複数 PR の実験。Q4 はそのまま破壊的操作を弾きます。

## Q6. サイクル

[サイクルメニュー](cadence.html)を参照。

## Q7. エスカレーション トリガー

ループが押し通すのではなく、止まってあなたに知らせるべき場面。

- **連続失敗 3 回** — 同じ候補が 3 サイクル失敗 → NOT-OK に追加して次へ。全候補が失敗ならエスカレート。
- **Diff cap 超過** — 提案の変更が tier の上限を超える → まずサブタスクに分割、それでも超えるならエスカレート。
- **不可逆操作** — DB DDL、force-push、外部 API 書き込み — 実行前に必ずエスカレート。
- **候補なし**:
  - `end` *(デフォルト)* — ミッション完了とみなし、ScheduleWakeup を出さない。
  - `ask` — ユーザーに追加の探索ツールを尋ねる。
- **許可パス外の候補が 5 件以上** — ミッション範囲の拡張を提案。

## Q8. 自動コンパクション

長いミッションは prompt-too-long に当たるので、会話を定期的にトリムします。`/compact` を呼んで古い履歴を整理しつつ、直近の状態は残します。

- **threshold** — トークン使用率がこの % を超えたら pause-and-compact。
  - いつ? トークンが重い作業(大きな diff、巨大ファイル)は 60-70、通常の docs/コードサイクルは 80-90。デフォルト **80**。
- **frequency**:
  - `every-cycle` *(デフォルト)* — 毎サイクル軽く圧縮。コストが予測でき、長期セッションで最も安全。
  - `threshold-only` — 閾値を超えたときだけ圧縮。短いセッションでトークン節約。
  - `off` — 圧縮しない。短い bounded ミッション、もしくは自分で文脈を管理する場合のみ推奨。

## Q9. アップデートポリシー

GitHub releases で新バージョンが出ていないか、定期的に確認します。

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — デフォルト `every-24h`
  - いつ? 毎日触るリポは `every-24h`。新バージョンをすぐほしいなら `every-boot`。リリースサイクルが緩いなら `weekly`。手動で更新する派なら `off`。
- **on_update_available**:
  - `notify` — サイクル出力の末尾に 1 行通知を追加。*いつ?* 毎サイクル出力を読む運用。
  - `prompt` *(デフォルト)* — 通知を出して「今すぐアップデート?」を確認。承認すれば `npx skills update PresentJay/autopilot-skills --yes` を実行。*いつ?* たまに眺める運用で、明示的な同意がほしいとき。
  - `silent-auto` — 確認なしで自動実行。*いつ?* 信頼できるセットアップで、ログを細かく見ないとき。

チェックは fail-open: GitHub API エラーや 5 秒タイムアウトのときは静かにスキップして、次回リトライします。サイクルを絶対に止めません。

## Q10. 再開ポリシー

ホスト sleep・セッションクラッシュ・ScheduleWakeup の取りこぼし・サイクル中断 —— こうした中断からどう立ち直るかを決めます。

- **stale_threshold**: `2x-cadence` *(デフォルト)* / `4x-cadence` / `8x-cadence` — `next_wakeup_at` からどれだけ経過したら stalled とみなすか。
  - いつ? 積極的に復旧したいなら `2x-cadence`(1 サイクル取りこぼし = stalled)。インフラが安定していて時々負荷がかかる程度なら `4x-cadence`。サイクル長めで夜間ホスト sleep が常態なら `8x-cadence`。
- **on_resume**:
  - `auto-resume` *(デフォルト)* — stale を見つけたら静かに新サイクルを開始。*いつ?* ループを信頼していて、流れを止めたくないとき。
  - `prompt-confirm` — 診断を出して(「N サイクル取りこぼし。再開?」)確認後に続行。*いつ?* 復旧のたびに把握したいとき。
  - `manual-only` — `/autopilot resume` または `/autopilot heal` の明示シグナルがあるときだけ復旧。*いつ?* 意図的に pause したミッションを、自分のタイミングで再開したいとき。

Phase 0.5 が 5 つのパターンを拾います: crashed mid-cycle・missed wakeups・schedule lost・paused・escalated。

ユーザーシグナル: `/autopilot resume`・`/autopilot heal`・`/autopilot status`・`/autopilot version`。
