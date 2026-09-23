# 贡献规则

1. 活动代码只在 `frog/`、`tests/`、`lab/`、`docs/` 中修改；`archive/` 与 `assets/archive/` 视为只读档案。
2. 每个代码变更先写失败 pytest，再做最小实现，并运行全量测试。
3. 每个实验必须新增/更新对应 `docs/experiments/stage*.md`，写明假设、输入、奖励、基线、指标与停止条件。
4. 禁止将 `random_search` 描述为完整自然演化。
5. 提交前执行：

```bash
python -m pytest
python -m compileall -q frog tests
python scripts/validate_repo.py
python scripts/check_links.py
python -m frog search --seed 123 --max-attempts 50000 --json
git diff --check
```

提交格式：`feat(stage-00): ...`、`test: ...`、`docs: ...`、`refactor: ...`。