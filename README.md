# ncompile: Topological QEC Compiler

`ncompile` is a research-in-progress compiler toolchain built on **MLIR** for mapping, scheduling, and optimizing Topological Quantum Error Correction (QEC) codes. It focuses on quantifying and mitigating the "Topological Tax"—the physical latency and noise overhead introduced by routing and braiding operations on hardware grids like the **Microsoft Tetron** Majorana architecture.

## The Problem: The Topological Tax

In topological quantum computing, operations are performed by **braiding** quasiparticles (like Majorana Zero Modes) around one another. Unlike traditional superconducting qubits where any two adjacent qubits can interact, topological hardware has strict spatial constraints:
1.  **Resource Sharing**: A single MZM cannot be involved in multiple parity measurements simultaneously.
2.  **Path Collisions**: The physical path taken to braid two MZMs together "blocks" a region of the 2D grid, preventing other operations in that area.

Standard compilers ignore these "taxes," leading to unrealistic performance estimates. `ncompile` uses MLIR to model these constraints explicitly, reducing circuit depth and improving the topological threshold.

## The QEC Dialect

The core of `ncompile` is the `qec` dialect, which provides high-level primitives for fault-tolerant circuits:
- `qec.mzm`: Represents a Majorana Zero Mode at a specific `(x, y)` coordinate.
- `qec.measure_parity`: A multi-target operation representing a stabilizer check.
- `qec.detector`: Compares measurement results across rounds to identify errors.
- `qec.logical_observable`: Defines the logical parity of the code.

## The Scheduling Pipeline (`qeccc-opt`)

The primary optimization is the `--qec-schedule` pass. It transforms a sequential list of QEC operations into a parallelized schedule by assigning each operation a `time_slice`.

### 1. Footprint Generation
The compiler calculates the "spatial footprint" of every operation.
- **ASAP Mode**: The footprint is just the endpoint MZMs.
- **Braiding Mode**: The footprint includes the entire routing path on the 2D grid required to perform the braid.

### 2. Conflict Graph Construction
A graph is built where each node is a QEC operation. An edge is added between two operations if their spatial footprints overlap (i.e., they share an MZM or their braiding paths collide).

### 3. Greedy Coloring
The pass performs a greedy coloring of the conflict graph. The "color" assigned to each node becomes its `time_slice` (the clock cycle it executes in). This ensures that no two conflicting operations ever run in parallel.

## Usage Guide

### 1. Installation
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mkdir build && cd build
cmake .. -G Ninja -DMLIR_DIR=/path/to/mlir
ninja
```

### 2. Basic Compilation
To schedule an MLIR file using the default greedy scheduler:
```bash
./build/bin/qeccc-opt --qec-schedule examples/surface_d3.mlir > scheduled.mlir
```

### 3. Advanced Scheduling Options
- `--qec-schedule="asap=true"`: Ignores braiding paths, assuming instant routing (physical baseline).
- `--qec-schedule="use-astar=true"`: Uses congestion-aware A* routing to minimize path collisions.
- `--qec-schedule="naive=true"`: Assigns each operation to its own unique time slice (serial execution).

### 4. Translation to Stim
To generate a `.stim` file for simulation:
```bash
./build/bin/qeccc-translate --qec-to-stim scheduled.mlir > circuit.stim
```

## Simulation & Results

`ncompile` includes an end-to-end simulation runner that automates the sweep from Stim → MLIR → Scheduling → Stim → PyMatching:

```bash
python3 tools/run_simulations.py
```

| Distance | Baseline Depth (ticks) | Scheduled Depth (ticks) | Reduction |
|---|---|---|---|
| d=3 | 14 | 7 | 2.0x |
| d=5 | 14 | 10 | 1.4x |

### Threshold Sweep Results
![Surface Threshold Sweep](docs/images/surface_threshold_final.png)

## Development Roadmap

- [ ] **Full CNOT Reordering**: Physically manifest the depth reduction by reordering gates in the Stim circuit while preserving detectors.
- [ ] **qLDPC Code Support**: Extend the importer and scheduler to support more complex non-local parity check codes.
- [ ] **Automated Braiding Verification**: Add a pass to verify that no two scheduled braids ever physically collide on the grid.

## Examples

The `examples/` directory contains sample MLIR files for various surface code distances:
- `examples/surface_d3.mlir`: A distance-3 surface code before scheduling.
- `examples/surface_d3_scheduled.mlir`: The same code after running the `--qec-schedule` pass.

## Contributing

We welcome contributions! Please install `pre-commit` to ensure code quality:
```bash
pip install pre-commit
pre-commit install
```
To ensure consistent C++ code style, please use `clang-format` before submitting a pull request:
```bash
find lib include -name "*.cpp" -o -name "*.h" | xargs clang-format -i
```

## Citation

If you use `ncompile` in your research, please cite this work. Citation is required for academic or commercial use of this software.

```bibtex
@software{ncompile2026,
  author = {Washim Neupane},
  title = {ncompile: A Topological QEC Compiler based on MLIR},
  year = {2026},
  url = {https://github.com/washim/ncompile}
}
```

---
*Developed for research on fault-tolerant topological QEC architectures.*
