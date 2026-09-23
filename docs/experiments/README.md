# 实验索引

每个阶段都有**代码、测试、配置、文档与统一 CLI 演示**。执行统一入口：

```bash
python scripts/run_stage.py 00
python scripts/run_stage.py 01
python scripts/run_stage.py 02
python scripts/run_stage.py 03
python scripts/run_stage.py 04
python scripts/run_stage.py 05
python scripts/run_stage.py 06
python scripts/run_stage.py 07
```

```mermaid
flowchart LR
  S00[00 确定性内核] --> S01[01 生命周期]
  S01 --> S02[02 种群/突变]
  S02 --> S03[03 局部感知]
  S03 --> S04[04 避险行为]
  S04 --> S05[05 树分裂发育]
  S05 --> S06[06 单像素反射]
  S06 --> S07[07 双像素反射]
  S07 -.历史等价检查.-> S08[08 random_search]
```

| Stage | 主题 | 代码 | 配置 | 文档 | 当前性质 |
|---:|---|---|---|---|---|
| 00 | 确定性仿真内核 | `stage00_kernel` | `stage00-kernel.json` | [说明](stage00-kernel.md) | 已实现基础内核 |
| 01 | 能量、食物、死亡 | `stage01_lifecycle` | `stage01-lifecycle.json` | [说明](stage01-lifecycle.md) | 已实现规则环境 |
| 02 | 选择与有界突变 | `stage02_evolution` | `stage02-evolution.json` | [说明](stage02-evolution.md) | 已实现教学型种群机制 |
| 03 | 局部观察与行动 | `stage03_sensor_action` | `stage03-sensor-action.json` | [说明](stage03-sensor-action.md) | 已实现防信息泄漏接口 |
| 04 | 单一避险行为 | `stage04_behavior` | `stage04-behavior.json` | [说明](stage04-behavior.md) | 已实现最小行为任务 |
| 05 | 二叉树发育 | `stage05_development` | `stage05-development.json` | [说明](stage05-development.md) | 已实现确定性表型布局 |
| 06 | 单像素反射 | `stage06_one_pixel_reflex` | `stage06-one-pixel-reflex.json` | [说明](stage06-one-pixel-reflex.md) | 已实现透明统计基线 |
| 07 | 双像素反射 | `stage07_two_pixel_reflex` | `stage07-two-pixel-reflex.json` | [说明](stage07-two-pixel-reflex.md) | 已实现查表/混淆矩阵基线 |
| 08 | 原 018 等价随机搜索 | `frog/search.py` | CLI 参数 | [根 README](../../README.md) | 固定场景 `random_search` |

## 重要边界

Stage 02、06、07 目前是**最小可运行基线**，目的是将作者的概念拆成可测试接口，并不等价于完成了复杂进化、神经学习或模式泛化。每一阶段在下一轮迭代前都应按 [研究证据契约](../research-contract.md) 增补 baseline、30 个 seed、独立测试集和 telemetry。