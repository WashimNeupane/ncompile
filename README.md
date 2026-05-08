# NCompile - MLIR Compiler Boilerplate

NCompile is a starting point for building custom MLIR-based compilers. It provides a skeleton dialect, an optimizer driver (`ncompile-opt`), and a testing framework.

## Prerequisites

Before building, ensure you have the following installed:

- **Python 3.x**
- **C++ Compiler** (e.g., MSVC on Windows, GCC/Clang on Linux)
- **CMake** (>= 3.20)

### Install Build Tools
You can install the necessary build tools via pip:
```powershell
pip install -r requirements.txt
```

## Setting up LLVM and MLIR

This project requires a build of LLVM and MLIR with development headers.

### 1. Clone LLVM Project
```powershell
git clone https://github.com/llvm/llvm-project.git
```

### 2. Build LLVM/MLIR
From the `llvm-project` directory:
```powershell
mkdir build
cd build
cmake -G Ninja ../llvm \
  -DLLVM_ENABLE_PROJECTS=mlir \
  -DLLVM_BUILD_EXAMPLES=ON \
  -DLLVM_TARGETS_TO_BUILD=Native \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_ASSERTIONS=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DLLVM_USE_LINKER=lld

cmake --build .
```

## Building NCompile

Once LLVM/MLIR is built, you can build NCompile:

1. **Create a build directory**:
   ```powershell
   mkdir build
   cd build
   ```

2. **Configure with CMake**:
   Provide the path to your LLVM/MLIR build directory:
   ```powershell
   cmake -G Ninja .. \
     -DMLIR_DIR=<path_to_llvm_project>/build/lib/cmake/mlir \
     -DLLVM_DIR=<path_to_llvm_project>/build/lib/cmake/llvm
   ```

3. **Build**:
   ```powershell
   ninja
   ```

## Running Tests

To run the custom optimizer driver:
```powershell
./bin/ncompile-opt ../test/ncompile-opt/dummy.mlir
```

To run the full test suite:
```powershell
ninja check-ncompile
```

## Project Structure

- `include/`: Dialect definitions and headers.
- `lib/`: Dialect implementation.
- `ncompile-opt/`: Driver tool source.
- `test/`: Regression tests.
- `legacy/`: Old project files (ignored by git).
