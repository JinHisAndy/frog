# Java 到 Python 的迁移说明

## 迁移范围

本 fork 的可维护实现已从 Java/Maven 迁移为 Python。迁移目标是保留当前 018 原型的**核心实验语义**，并把它拆为可测试的小模块，而不是逐行翻译 743 个历史 Java 文件。

现在的维护入口：

```text
frog/
  model.py        # 节点、连接、化学标签、观察、动作、回放帧
  network.py      # 阈值网络、传播和受调制的权重变化
  search.py       # 确定性 random_search、训练场景与盲测场景
  replay.py       # 逐步回放数据
  cli.py          # search / replay / gui 命令
  visualizer.py   # 可选 tkinter 网络回放界面
```

## 保留的核心含义

Python 原型保留了当前 `core/EvolutionWindow1.java` 的以下概念：

- 四个二值视觉像素，以及 `pain`、`sweet` 两个反馈输入；
- 两个行为输出：`flee` 与 `bite`；
- 阈值节点、带权有向连接和中继层；
- `dopamine`、`norepinephrine`、`glutamate`、`gaba` 化学标签；
- 当相应化学标签活跃时、权重按受限区间 `[0, 100]` 变化的可塑性规则；
- 训练场景：`1100 + pain`、`0111 + sweet`；
- 盲测场景：敌人只逃、食物只咬、噪声不动作，且盲测时 `pain/sweet` 均为 `false`；
- 可序列化网络和逐步回放帧；
- tkinter 可用时的网络回放界面，或无显示环境中的安全降级提示。

## 明确不作的声明

新代码的候选发现器名为 **`random_search`**。它每次在固定 seed 下随机生成小网络，执行两次训练场景，再筛选能通过固定盲测的候选；它**不是**完整的种群遗传、跨代繁殖、细胞分裂式发育或开放式自然演化。

因此，本 fork 不将一次或多次候选网络的通过解释为：

- 生物神经回路的高保真模拟；
- 已经验证的条件反射泛化；
- 通用智能；
- 自我意识；
- AGI。

后续要证明更强结论，须遵守 [docs/03-experiment-contract.md](docs/03-experiment-contract.md) 的独立 seed、基线、训练/验证/测试隔离和量化要求。

## 移除的内容

按 fork 维护者要求，已从 Git 工作树删除：

- 所有追踪的 `*.java` 源文件；
- 所有 `pom.xml`；
- 所有 `run.bat`、`run.sh`；
- 所有 Maven clean/eclipse 辅助批处理文件。

这包含根 `core/` 与 `history/` 下的 Java/Maven 实现快照。未保留 Java 源码副本。

## 保留的档案

保留原始的说明、理论记录、许可证、文档、历史目录命名和 GIF/PNG/JPG 素材。它们是作者探索过程的**参考档案**；历史文档中关于 Java、Maven 和运行脚本的文字属于当时叙事，不应再作为当前维护入口。

当前实际运行方式以 `README.md` 顶部、`pyproject.toml` 和 `frog/` 包为准。