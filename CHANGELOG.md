# Changelog

本项目采用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 的简化格式。

## [Unreleased]

### Planned

- Stage 01：能量、食物与生命周期；
- 将当前平铺 Python 包迁移为更严格的 `src/` 布局（由 CLI 合同测试保护）；
- 为实验输出增加 30-seed 批量 telemetry。

## [0.2.0] - 2026-09-23

### Changed

- 建立 Python-first 活动代码、文档、资产和历史档案边界；
- 删除失效 Java/Maven/启动脚本残留；
- 将历史素材与叙事迁入 `assets/archive/`、`archive/`；
- 随机网络强制严格前向分层连接，避免输入重复传播；
- Replay 改为使用搜索时真实记录的训练快照，而非从最终网络重新训练。

### Added

- Stage 00 确定性网格仿真内核、配置和测试；
- 仓库验证、Markdown 链接检查和 GitHub Actions；
- 架构、实验门禁、证据契约、迁移和档案文档。

## [0.1.0] - 2026-09-23

### Added

- Java 018 原型的 Python 等价 `random_search`、JSON CLI、回放与 tkinter 展示；
- pytest 基础验证和 Java→Python 迁移说明。
