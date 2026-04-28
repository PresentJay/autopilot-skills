---
title: マイルストーン
---

# マイルストーン

サイクルが 4 つのトリガーいずれかに該当すると、ジャーナルエントリは**追加で** `.autopilot.milestones/<date>-<slug>.md` にも書かれます。このフォルダは固定で、`mission.md` から場所を変更できません。

## トリガー

1. **PR がマージ** — 追跡中の PR が `MERGED` に遷移したサイクル。
2. **Bounded ミッション完了** — Q2=bounded N に到達し、すべてグリーン。
3. **初の zero-defect 達成** — 追跡中の欠陥カテゴリ(lint、test、type、coverage)で初めて 0 を達成。`state.json` の `defect_baselines.<category>.ever_zero` で追跡。
4. **新規の NOT-OK パターン** — `mission.md` に初めて追加されたアンチパターン。

## なぜ固定か

マイルストーンは「何が重要だったか」のキュレーションされた軌跡です。`mission.md` で経路変更を許すとユーザーが履歴を隠せてしまうため、不変性が監査ログを守ります。
