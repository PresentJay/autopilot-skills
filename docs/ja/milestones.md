---
title: マイルストーン
---

# マイルストーン

サイクルが 4 つのトリガーのどれかに当たると、ジャーナルエントリは `.autopilot.milestones/<date>-<slug>.md` にも書かれます。このフォルダは固定で、`mission.md` から場所を変えられません。

## トリガー

1. **PR がマージ** — 追跡している PR が `MERGED` に切り替わったサイクル。
2. **Bounded ミッション完了** — Q2=bounded N に到達して、すべてグリーン。
3. **初の zero-defect 達成** — 追跡している欠陥カテゴリ(lint・test・type・coverage)で初めて 0 になった瞬間。`state.json.defect_baselines.<category>.ever_zero` で追跡。
4. **新しい NOT-OK パターン** — `mission.md` に初めて追加されたアンチパターン。

## なぜ固定か

マイルストーンは「何が大事だったか」を残すキュレーションされた跡です。`mission.md` で経路を変えられると、ユーザーが履歴を隠せてしまう —— 不変性が監査ログを守ります。
