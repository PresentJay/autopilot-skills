---
layout: page
title: "入门"
lang: zh
---

能在本次执行中完成的工作只读取技能入口并检查结果，不创建状态或日志文件，也不对整个工作目录计算哈希。持久记录用于跨会话交接、定期监控、用户明确要求记录或已有任务。始终保留已有暂停状态和用户修改。

V2是正在审核的预览版，默认分支仍为v1.3。请明确安装预览分支:

```sh
git clone --branch improve/codex-missions-v2 https://github.com/PresentJay/autopilot-skills.git autopilot-skills-v2
npx skills add ./autopilot-skills-v2 --skill autopilot
```

在Codex中使用`$autopilot`，在Claude Code中使用`/autopilot`。说明目标、允许范围、完成检查和停止条件。代码、研究和文档均可使用，不要求Git。

普通任务会持续推进，直到完成验证、遇到阻碍、暂停或达到用户或宿主的执行限制。不会仅因到达检查点而停止。`run-once`仅运行一个检查点。跨轮次继续执行时，请明确请求宿主提供的native goal。定时执行是另一项能力。

对于明确的一次性任务，原生goal可能已经足够。Autopilot提供可复用的任务说明和工作记录。尚未证明速度或结果更好，请查看[比较结果与限制](../evidence.html)。
