# 项目架构

公开版只保留一条最容易讲清楚、也最适合面试展示的执行链路：

1. 读取公开 sample unit
2. 分析 `description.json` 与 `label_infos.json`
3. 获取录屏元信息
4. 计算 stall / resolution 初筛分
5. 抽取关键帧并生成 storyboard
6. 输出 JSON / Markdown 报告
7. 通过 Flask API 对外暴露 demo 入口

## 模块分层

### `samples/units`

放公开的 sample unit。  
这里的 unit 结构尽量贴近真实产物，但内容已经做成适合公开展示的 demo 数据。

### `common/prescreen_runner.py`

核心业务层。

- 读取样本
- 评分
- 生成图片证据
- 组织结构化返回

### `common/job_queue.py`

做一个最小化 job lifecycle：

- enqueue
- list
- process
- query detail

它不是完整调度系统，但足够把仓库叙事拉到“服务层”。

### `app/server.py`

把 prescreen runner 包成一个可直接体验的 Flask API。

### `tests/`

覆盖 runner 和 API 的基础行为，保证公开版仓库可回归。

## 为什么这样拆

原始仓库里有完整的多服务结构，但直接公开会有两个问题：

1. 依赖环境太重
2. 叙事焦点不集中

所以公开版只保留最能体现工程能力的一段链路，把它做成一个能讲、能跑、能测的小项目。

