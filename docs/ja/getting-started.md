---
title: はじめに
---

# はじめに

## インストール

```bash
npx skills add PresentJay/autopilot-skills
```

プロンプトでハーネスを選択するか、`--all -g` で全ハーネスに一括インストール。

## ミッションを開始する

ハーネス(Claude Code、Codex、Cursor など)で:

```
/autopilot
```

初回は 8 問のインタビューが始まります。すでに決めている回答は引数で渡し、その質問をスキップできます:

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## 停止する

- "stop autopilot" / "멈춰" / "pause" — `mission.md` の Mode を `paused` に変更。
- `.autopilot.log/mission.md` を削除 — 次回呼び出しでコールドスタート。
