# 快速上手

## 1. 创建环境

```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
```

选择 VS Code 中的 `.venv` 解释器，并使用 Testing 面板运行 pytest。

## 2. 运行当前原型

```bash
python -m frog search --seed 123 --max-attempts 50000 --json
python -m frog replay --seed 123 --max-attempts 50000 --json
python -m frog gui --seed 123 --max-attempts 50000
```

`search` 是固定 seed 的候选搜索；`replay` 读取搜索阶段保存的真实训练快照，再生成无学习的盲测回放；`gui` 仅用于展示，不能作为实验成功证据。

## 3. 正确解读输出

搜索 JSON 中必须读取：

- `method`：当前必须为 `random_search`；
- `seed` 与 `attempts`：可复现搜索条件；
- `training_trace`：实际发生的训练前后快照；
- `blind_inputs`：盲测中 `pain/sweet` 均应为 `false`；
- `blind_test`：固定敌人、食物、噪声情境上的动作。

通过这三组固定情境只说明候选通过了该小型检查，不说明它具备泛化或完整演化能力。

## 4. 开始新实验

不要修改 `archive/`。从 `lab/` 新建阶段目录，先写测试与假设，再写实现。每个阶段的模板与门禁见 [实验索引](experiments/README.md)。