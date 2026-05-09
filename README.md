# ncompile: Topological QEC Compiler

`ncompile` is a specialized compiler toolchain for mapping and scheduling Topological Quantum Error Correction (QEC) codes onto physical hardware grids, specifically the **Microsoft Tetron** Majorana architecture.

## Research Breakthrough: The Topological Tax
Conventional QEC compilers often ignore the physical cost of topological braiding. We built an MLIR-based toolchain that quantifies this cost; revealing a significant latency increase for high-rate codes and introduced **braiding-aware scheduling** to mitigate physical routing bottlenecks.

### Key Results
- **Grid Tax**: Mapping logical checks to a 2D grid increases depth by ~6x.
- **Braiding Tax**: Braiding paths for high-weight checks (weight-12) can add significant overhead.
- **Optimization**: Our **MIS-based scheduler** achieves **~50 cycles per round** for the [[72, 12, 6]] Bivariate Bicycle code. We discovered that **direct L-shaped routing** outperforms complex A* pathfinding by minimizing the global conflict footprint.

## Threshold Analysis
We verified the physical threshold of the Tetron grid using a topological repetition code benchmark.

![Threshold Plot](research_artifacts/threshold_plot.png)

## Scaling & Performance
`ncompile` achieves near-linear scaling, enabling the compilation of large-scale qLDPC codes in seconds, whereas SMT-based baselines (like ASC) exhibit exponential latency.

![Scaling Plot](research_artifacts/scaling_plot.png)

## Installation
```bash
mkdir build && cd build
cmake .. -G Ninja -DMLIR_DIR=/path/to/mlir
ninja
```

## Usage
### 1. Generate Gross Code
```bash
python3 tools/gen_tetron_gross_code.py > gross.mlir
```

### 2. Schedule for Tetron Grid
```bash
build/bin/qeccc-opt --qec-schedule gross.mlir
```

### 3. Simulate with Stim
```bash
build/bin/qeccc-translate --to-stim gross.mlir > circuit.stim
stim sample --shots 10000 --circuit circuit.stim
```

---
*Developed for Phase 4 Research on Topological QEC Architectures.*
