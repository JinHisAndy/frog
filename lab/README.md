# Lab workspace

`lab/` is the clean workspace for future Stage 01—07 experiments. It contains no active implementation yet; Stage 00 lives in `frog/experiments/stage00_kernel/` because it establishes reusable core conventions.

Each future stage should create:

```text
lab/stageNN-name/
  README.md          # hypothesis, baseline, metrics, stop condition
  config.json        # versioned parameters
  notes.md           # interpretation and failure analysis
```

The runnable implementation belongs in `frog/experiments/stageNN_name/`, tests in `tests/`, and generated telemetry in ignored `runs/`.