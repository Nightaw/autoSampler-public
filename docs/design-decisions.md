# 设计取舍

## 1. 不直接公开原始多服务目录

原始项目里有 `master / slave / sniffer / transfer` 等服务。  
这些内容在工作仓库里有价值，但放到个人 GitHub 展示里会显得过重，而且需要更多环境解释。

公开版改成一条更短、更完整的链路：

- sample unit
- prescreen runner
- report
- API

这样更容易在几分钟内讲清楚。

## 2. 保留服务层，而不是只保留脚本

如果只有一个 `label_prescreen.py`，仓库会像工具脚本集合。  
补上 mock API、job queue、device registry 和 scenario planner 后，更像真实项目，也更利于展示“工程化组织能力”。

## 3. 远端 SSH / 模型补评分不放进默认主线

工作仓库里的远端拉样本、模型视觉补评分都很有价值，但公开版默认主线尽量保证：

- 本地即可运行
- 依赖简单
- 结果稳定

所以公开版以本地 sample unit 为默认路径，把复杂能力留在文档说明里，而不是要求使用者先配环境。

## 4. Storyboard 作为“可选增强”

如果本机有 `ffmpeg` / `ffprobe`，会生成 storyboard。  
如果没有，runner 仍然可以完成报告生成。

这样仓库对外部环境更宽容。

## 5. 使用多个 sample unit，而不是单一 happy path

公开版现在保留两类样例：

- 规则较干净的 baseline case
- 需要人工复核的 resolution review case

这样仓库展示的不只是“能跑通”，还包括“能发现问题”。
