---
layout: page
title: "はじめに"
lang: ja
---

V2はレビュー中のプレビューです。デフォルトブランチはまだv1.3です。プレビューを明示的にインストールしてください:

```sh
git clone --branch improve/codex-missions-v2 https://github.com/PresentJay/autopilot-skills.git autopilot-skills-v2
npx skills add ./autopilot-skills-v2 --skill autopilot
```

Codexでは`$autopilot`、Claude Codeでは`/autopilot`を使います。成果、許可する範囲、完了の確認方法、停止条件を伝えてください。コード・調査・文書を対象とし、Gitは必須ではありません。

通常のミッションは、完了の確認、障害、一時停止、ユーザーまたはホストの実行上限まで続けます。チェックポイントだけを理由に停止しません。`run-once`は1回に限定します。ターンをまたぐ実行には、対応するホストのnative goalを明示的に依頼してください。予約実行は別の機能です。

明確な単発タスクでは標準のgoalで十分な場合があります。Autopilotは再利用できるミッション定義と作業記録を追加します。速度や成果の優位性は未確認です。[比較結果と制約](../evidence.html)を確認してください。
