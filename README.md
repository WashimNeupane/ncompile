# NCompile - QEC Research Compiler

**Author:** Washim Neupane (washimneupane@outlook.com)

NCompile is a specialized MLIR-based compiler infrastructure designed for Quantum Error Correction (QEC) research. It acts as a bridge between abstract parity-check specifications and cycle-accurate hardware gate schedules.

## Core Concepts

### The QEC Dialect
The compiler centers around the `qec` dialect, which provides types and operations specifically for fault-tolerant quantum computing:
- **Physical Coordinates**: Qubits are tracked via `!qec.qubit<x, y>` types, allowing for geometry-aware optimizations.
- **High-Level Paulis**: Parity checks are defined using `qec.measure_pauli`, abstracting away the complex CNOT sequences until the scheduling phase.
- **Hardware Primitives**: Supports lowering to standard gates like `cx`, `reset`, and `measure`.

### Automated Scheduling
The core research value of NCompile is its automated scheduling pass. It transforms a set of overlapping Pauli measurements into an optimal, non-conflicting gate schedule by:
1. Building a **Conflict Graph** of shared qubits.
2. Applying **Graph Coloring** to assign measurements to time slices.
3. Expanding Paulis into hardware-specific CNOT cascades.

### Testing & Verification
We use a multi-tier approach to ensure compiler correctness:
- **Lit Tests**: IR-level regression testing.
- **Stim Integration**: Direct lowering to `.stim` files for Monte-Carlo simulation of error rates.
- **Verifiers**: Strict C++ checking of hardware constraint violations.

## Prerequisites

- **LLVM/MLIR**: Built with `MLIR_ENABLE_BINDINGS_PYTHON=ON`.
- **Python 3.10+**
- **nanobind**: Installed via pip or available in the system.
- **Ninja & CMake**

## Building the Compiler

1. **Setup Environment**:
   Ensure your `MLIR_DIR` and `LLVM_DIR` point to your LLVM build.

2. **Configure**:
   ```bash
   mkdir build && cd build
   cmake -G Ninja .. \
     -DMLIR_DIR=/path/to/llvm-project/build/lib/cmake/mlir \
     -DLLVM_DIR=/path/to/llvm-project/build/lib/cmake/llvm \
     -DMLIR_ENABLE_BINDINGS_PYTHON=ON
   ```

3. **Build**:
   ```bash
   ninja
   ```

## Python Integration

To use the QEC Python bindings, add the following to your `PYTHONPATH`:
```bash
export PYTHONPATH=$MLIR_PYTHON_PACKAGES:$NCOMPILE_BUILD/python/python_packages
```

### Generating Benchmarks
You can generate the Gross code benchmark IR using the provided tool:
```bash
venv/bin/python3 tools/gen_gross_code.py > benchmarks/gross_72_12_6.mlir
```

## Documentation

API documentation is generated using Doxygen. To build the documentation:
```bash
ninja doxygen
```
The output will be available in `docs/html/index.html`.

## Testing

Run the QEC-specific test suite:
```bash
ninja check-qeccc
```

## Project Structure

- `include/ncompile/Dialect/QEC`: C++ Dialect definitions (ODS).
- `include/ncompile-c/Dialect/QEC`: C-API for Python interoperability.
- `lib/Dialect/QEC`: Dialect implementation.
- `python/ncompile/dialects`: Python wrappers and generated ODS.
- `tools/`: Research scripts and benchmark generators.
- `test/`: Lit regression tests.
