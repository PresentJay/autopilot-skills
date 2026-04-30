---
title: はじめに
---

# はじめに

## インストール

```bash
npx skills add PresentJay/autopilot-skills
```

プロンプトでハーネスを選ぶか、`--all -g` で一気に全部入れます。

## ミッションを開始

使っている AI(Claude Code・Codex・Cursor など)で:

```
/autopilot
```

初回は 10 問のセットアップが立ち上がります。すでに決めている回答は引数で渡せば、その質問だけスキップできます。

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## 止める

- "stop autopilot" / "멈춰" / "pause" — `mission.md` の Mode が `paused` に変わります。
- `.autopilot.log/mission.md` を消す — 次回呼び出しで最初から。
