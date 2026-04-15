# Worker API Demo

## `GET /health`

健康检查。

响应：

```text
ok
```

## `GET /demo/scenarios`

返回内置 demo 场景。

响应示例：

```json
{
  "scenarios": [
    {
      "name": "baseline_prescreen",
      "title": "Baseline Label Prescreen"
    }
  ]
}
```

## `POST /demo/run`

直接运行一次 mock prescreen。

请求示例：

```json
{
  "scenario": "baseline_prescreen"
}
```

## `POST /demo/jobs`

创建一个排队 job。

## `POST /demo/jobs/process`

处理队列里的下一个 job。

## `GET /demo/jobs/<job_id>`

查询 job 详情。

## `GET /demo/report.md?scenario=baseline_prescreen`

返回 Markdown 版本报告，适合直接在浏览器或文档系统里查看。

