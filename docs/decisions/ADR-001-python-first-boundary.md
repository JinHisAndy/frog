# ADR-001：Python-first 活动边界

- **状态**：已接受
- **背景**：原项目包含大量 Java/Maven 快照；迁移后 Java 源已删除，但残留脚本和文档仍混入活动入口。
- **决策**：Python `frog/`、`tests/`、`docs/`、`lab/` 构成唯一活动面；历史叙事和素材迁入 `archive/`、`assets/archive/`，不参与运行。
- **后果**：根 README 更清楚；历史 Java 通过 Git 查询；旧脚本不再可用。