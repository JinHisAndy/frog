# Frog 学习与重建入口

> 本 fork 的**可维护实现**已经迁移到根目录 `frog/` Python 包；原项目的 `history/`、`record/`、`other/`、README 与 GIF/图片保留为历史参考。本入口用于在 VS Code 中逐步实现并验证作者的人工生命思路，而不是把历史演示直接当作已证实的智能结论。

## 你将完成什么

从一个确定性的随机网络搜索原型开始，逐步建立：

```text
可复现实验 → 能量/生命周期 → 遗传与突变 → 感知—动作闭环
→ 发育式（树分裂）基因型 → 单像素条件反射 → 双像素条件反射
```

每一步都有明确假设、单元测试、量化指标、可视化证据和停止条件。当前 Python 迁移实现保留 018 的“四像素 + 痛/甜训练 + 盲测筛选”核心语义，但它明确是 `random_search`，不是完整遗传演化。阶段终点是一个能经独立训练/验证/测试证明的“小型条件反射系统”；**不以“通用智能”或“意识”作为任何阶段验收条件**。

## 从这里开始

1. [新手与环境准备](docs/00-start-here.md)
2. [原始项目与历史素材地图](docs/01-original-project-map.md)
3. [逐步实验路线图](docs/02-experiment-roadmap.md)
4. [实验可复现性契约](docs/03-experiment-contract.md)
5. [VS Code 工作流](docs/04-vscode-workflow.md)
6. [目标代码架构](docs/architecture-target.md)
7. [Java→Python 迁移边界](MIGRATION_TO_PYTHON.md)
8. [协作与实验规则](CONTRIBUTING_LEARNING.md)

## 两条工作线

- **参考线**：阅读原始 `history/<版本>/` 的 README、理论记录和素材，理解作者每一版试图解决什么。它们是只读历史证据，Java 实现已按 fork 的迁移策略移除。
- **重建线**：从根目录 `frog/` Python 包开始，逐步补充 `lab/` 中的可测实验。不要在 `history/` 中继续开发。

## 当前可运行入口

```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

python -m pytest
python -m frog search --seed 123 --max-attempts 50000 --json
python -m frog replay --seed 123 --max-attempts 50000 --json
python -m frog gui --seed 123 --max-attempts 50000
```

- `search`：输出随机搜索过程和敌人/食物/噪声盲测结果；
- `replay`：输出可供 UI 或分析工具消费的逐步事件帧；
- `gui`：有桌面显示时打开 tkinter 回放，没有显示时给出安全的 CLI 指引。

## 原项目的目标与我们的表述边界

作者希望借由“环境、遗传、突变、选择、可塑性”逐步获得复杂智能。这个方向值得实验，但历史 GIF、截图和单次成功运行**只能说明特定环境中发生过某种行为**，不能独立证明条件反射泛化、真实脑机制、意识或 AGI。我们会用可复现数据决定每一条结论的强度。