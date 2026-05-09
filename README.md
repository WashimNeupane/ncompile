# ncompile: Topological QEC Compiler

`ncompile` is a specialized compiler toolchain for mapping and scheduling Topological Quantum Error Correction (QEC) codes onto physical hardware grids, specifically the **Microsoft Tetron** Majorana architecture.

## Research Breakthrough: The Topological Tax
Conventional QEC compilers often ignore the physical cost of topological braiding. We built an MLIR-based toolchain that quantifies this cost; revealing a significant latency increase for high-rate codes and introduced **braiding-aware scheduling** to mitigate physical routing bottlenecks.

### Key Results
- **Grid Tax**: Mapping logical checks to a 2D grid increases depth by ~6x.
- **Braiding Tax**: Quantified at **~4.9x** (61 cycles ASAP vs 299 cycles Braided). Routing and braiding paths are the primary drivers of QEC latency.
- **Optimization**: Our **MIS-based scheduler** achieves **~50 cycles per round** for the [[72, 12, 6]] Bivariate Bicycle code.

## Threshold Analysis
We discovered that the **~4.9x Braiding Tax** significantly suppresses the topological threshold. Even at $p=10^{-6}$, the surface code remains above threshold due to accumulated idle noise during long braiding cycles.

![Surface Threshold Sweep](research_artifacts/surface_threshold_sweep.png)

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
