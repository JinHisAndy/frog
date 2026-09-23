# Frog：可复现的人工生命探索框架

Frog 是一个 **Python-first、实验驱动** 的人工生命探索项目。它把原作者长期积累的想法、失败记录和演示素材保留为档案，同时用可测试的 Python 实现，从最小可验证问题开始重建：感知、行动、反馈、可塑性、遗传与发育式结构。

> 当前已实现的 018 等价原型是一个**确定性随机网络搜索器**。它在固定小网络中搜索能通过三组固定盲测的候选，输出字段明确标记为 `method: "random_search"`。它不是完整的种群演化、不是生物脑仿真，也不能证明意识或 AGI。

## 快速开始

要求：Python **3.11+**。运行时仅依赖标准库；测试使用 `pytest`。

```bash
python -m venv .venv
# Linux/macOS
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
python -m pytest

# 查找并输出固定盲测证据
python -m frog search --seed 123 --max-attempts 50000 --json

# 输出真实训练轨迹与盲测回放帧
python -m frog replay --seed 123 --max-attempts 50000 --json

# 有桌面环境时打开 tkinter 回放；无桌面环境会提示 replay 命令
python -m frog gui --seed 123 --max-attempts 50000
```

## 当前能力与边界

| 已实现 | 未实现 / 不应声称 |
|---|---|
| 4 个二值视觉输入、痛/甜训练反馈、逃跑/咬合输出 | 通用智能、意识、AGI |
| 阈值节点、严格前向分层连接、化学调制标签 | 高保真生物神经科学模拟 |
| 真实训练快照、JSON 回放与可选 GUI | 完整遗传算法、跨代繁殖、细胞分裂发育 |
| 固定 seed、pytest、盲测中屏蔽痛/甜反馈 | 在未知环境中的模式泛化 |

## 项目结构

```text
frog/                   # 当前可运行 Python 包
  model.py              # 基础领域对象
  network.py            # 前向阈值网络与可塑性
  search.py             # 018 等价 random_search
  replay.py             # 真实训练轨迹与盲测帧
  cli.py                # search / replay / gui
  visualizer.py         # 可选 tkinter 回放

tests/                  # 当前行为、CLI、回放和边界测试
docs/                   # 当前用户、贡献者、实验与架构文档
lab/                    # 后续 Stage 00—07 干净实验空间
assets/                 # 原作者视觉素材与当前运行产物
archive/                # 历史叙事、版本说明、问答记录、旧资料；不可执行
configs/                # 后续版本化实验配置
runs/                   # 忽略的运行期 telemetry 输出
```

## 探索路线

项目不会一步跳向“人工意识”。每一阶段需要可失败的假设、测试、基线和量化记录后才能进入下一步：

1. 确定性仿真内核；
2. 能量、食物与生命周期；
3. 种群、选择与有界突变；
4. 局部观察与动作闭环；
5. 单一行为任务；
6. 树分裂/发育式结构编码；
7. 单像素条件反射；
8. 双像素条件反射与泛化评估。

Stage 00—07 均已有最小可运行 Python 实现、pytest、JSON 配置、文档和统一命令：

```bash
python scripts/run_stage.py 00  # 确定性内核
python scripts/run_stage.py 01  # 生命周期
python scripts/run_stage.py 02  # 选择与突变
python scripts/run_stage.py 03  # 局部感知
python scripts/run_stage.py 04  # 避险行为
python scripts/run_stage.py 05  # 树分裂发育
python scripts/run_stage.py 06  # 单像素反射
python scripts/run_stage.py 07  # 双像素反射
```

完整实验门禁见 [实验路线图](docs/experiments/README.md)。

## 文档入口

- [快速上手](docs/getting-started.md)
- [架构与依赖规则](docs/architecture.md)
- [实验索引与阶段门禁](docs/experiments/README.md)
- [可复现性与证据契约](docs/research-contract.md)
- [贡献规则](docs/contributing.md)
- [Java→Python 迁移说明](docs/migration-from-java.md)
- [历史档案导览](docs/archive-guide.md)
- [历史资料索引](archive/README.md)

## 许可证

本仓库使用 [Apache License 2.0](LICENSE)。历史档案中的随附许可证文本保留其原始位置；适用范围与迁移边界见 [档案导览](docs/archive-guide.md)。
