# 04：VS Code 实操工作流

## 1. 第一次打开

1. `File → Open Folder` 打开仓库根目录；
2. 安装 VS Code 的 Python 扩展；
3. 创建 `.venv` 并在 `Python: Select Interpreter` 中选择它；
4. 安装开发依赖：`python -m pip install -e ".[dev]"`；
5. 不要把 `history/` 当成当前代码工程；Java/Maven 源和脚本已被迁移策略移除，它们只保留文档/素材参考；
6. 当前维护代码从根目录 `frog/` 包开始，后续实验从 `lab/` 开始。

## 2. 运行当前原型

```bash
python -m pytest
python -m frog search --seed 123 --max-attempts 50000 --json
python -m frog replay --seed 123 --max-attempts 50000 --json
python -m frog gui --seed 123 --max-attempts 50000
```

VS Code 的 Testing 面板应能发现 `tests/` 下的 pytest 用例。

## 3. 创建新阶段

示例：

```bash
git switch -c lab/stage-00-kernel
mkdir -p lab/experiments/stage00-kernel
```

新阶段优先复用 `frog.model`、`frog.network` 的稳定接口。不要让 `lab/` 直接依赖历史目录；每阶段对应一个独立实验说明和配置目录。

## 4. 固定开发循环

```mermaid
flowchart LR
  A[写一条失败 pytest 测试] --> B[运行并确认失败]
  B --> C[最小实现]
  C --> D[测试通过]
  D --> E[无界面 CLI 批量运行]
  E --> F[输出 JSON/CSV]
  F --> G[最后增加 tkinter 或其他可视化]
  G --> H[小提交]
```

命令建议：

```bash
python -m pytest
python -m frog search --seed 123 --max-attempts 50000 --json

git diff --check
git status --short
git add frog tests docs
git commit -m "feat(stage-00): add deterministic simulation clock"
```

## 5. 什么时候打开 UI

只有满足以下条件后才做 GUI：

- 模拟内核在固定 seed 下可重复；
- 所有关键逻辑有 pytest 测试；
- headless CLI 批量运行已产出 JSON/CSV 指标；
- 可视化读取的是已记录运行数据或同一内核状态。

## 6. 每次工作结束前

- [ ] 测试通过；
- [ ] 结果目录写入 config/metadata/metrics；
- [ ] 新假设写进实验 README；
- [ ] `git diff --check` 无输出；
- [ ] 提交只包含本阶段的小变化。

完整规则见：[../CONTRIBUTING_LEARNING.md](../CONTRIBUTING_LEARNING.md)。