# Python 迁移验证记录

本文件记录 Java→Python 迁移时实际执行的验证命令和结果。它不把一次固定场景的成功描述为遗传演化、AGI 或生物机制证明。

## TDD 记录

### 1. 网络、随机性和可塑性

先创建 `tests/test_network.py`，其中要求：

- 同一 `SearchConfig(seed=123)` 得到相同搜索结果；
- 固定训练后，盲测满足敌人只逃、食物只咬、噪声不动作；
- 盲测输入显式为 `pain=false` 且 `sweet=false`；
- 只有活跃化学标签对应的连接更新，且权重夹紧在 `[0, 100]`。

在实现 `frog` 包前执行：

```bash
python3 -m pytest tests/test_network.py -q
```

实际结果：**失败**，错误为 `ModuleNotFoundError: No module named 'frog'`。这符合 RED 阶段：目标包尚不存在。

实现 `frog/model.py`、`frog/network.py`、`frog/search.py` 后执行同一命令：

```text
3 passed in 0.01s
```

### 2. 回放帧与 CLI JSON

先创建 `tests/test_replay_cli.py`，要求回放帧有连续序号、包含三个盲测场景，并且 CLI JSON 可解析。

在 `frog.__main__` 尚不存在时执行：

```bash
python3 -m pytest tests/test_replay_cli.py -q
```

实际结果：**1 failed, 1 passed**。失败原因为：

```text
python -m frog search ... returned non-zero exit status 1
```

这符合 RED 阶段：CLI 入口尚不存在。

实现 `frog/cli.py`、`frog/__main__.py`、`frog/visualizer.py` 后执行：

```bash
python3 -m pytest tests/test_replay_cli.py -q
```

实际结果：

```text
2 passed in 0.03s
```

## 最终验证

执行：

```bash
python3 -m pytest -q
python3 -m frog search --seed 123 --max-attempts 50000 --json
```

`pytest` 结果记录为：

```text
5 passed
```

固定 seed 的 `search` 命令成功输出可解析 JSON。结果包含：

- `method: "random_search"`；
- `seed: 123`；
- `found: true`；
- `attempts: 2`；
- `blind_inputs` 中敌人、食物、噪声三个场景的 `pain/sweet` 均为 `false`；
- `blind_test`：敌人 `{flee: true, bite: false}`，食物 `{flee: false, bite: true}`，噪声 `{flee: false, bite: false}`；
- JSON 安全的 `network.nodes` 和 `network.links`。

此外执行：

```bash
git diff --check
```

结果应为空输出，表示没有空白符错误。

## 覆盖映射

| 要求 | 测试/命令 |
|---|---|
| 固定 seed 可重复 | `test_same_seed_produces_same_search_result` |
| 敌人/食物/噪声映射 | `test_found_candidate_passes_blind_enemy_food_and_noise_cases` |
| 盲测不读取痛/甜 | 同一测试对 `blind_inputs` 的断言 |
| 化学调制与权重夹紧 | `test_plasticity_only_changes_links_for_active_chemical_and_clamps_weight` |
| 回放有序、含盲测 | `test_replay_frames_are_ordered_and_include_blind_frames` |
| CLI JSON 证据 | `test_search_cli_emits_parseable_random_search_evidence` |

后续 Stage 00—07 的环境、遗传和泛化实验必须另外补充 30 seed 批量评估，遵守 [03-experiment-contract.md](03-experiment-contract.md)。