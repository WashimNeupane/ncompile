# Setup TableGen for QEC Python ops
set(LLVM_TARGET_DEFINITIONS "${CMAKE_CURRENT_SOURCE_DIR}/../include/ncompile/Dialect/QEC/QECOps.td")
mlir_tablegen(ncompile/dialects/_qec_ops_gen.py -gen-python-op-bindings -bind-dialect=qec
  -I "${CMAKE_CURRENT_SOURCE_DIR}/../include"
  -I "${CMAKE_CURRENT_SOURCE_DIR}/../include/ncompile/Dialect/QEC"
)
add_public_tablegen_target(MLIRPythonQEC.tablegen)

# Declare the ncompile package sources
declare_mlir_python_sources(MLIRPythonNCompile.sources
  ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/ncompile"
  SOURCES
    __init__.py
    dialects/__init__.py
    dialects/qec.py
    dialects/_ods_common.py
)

# Declare the generated sources
declare_mlir_python_sources(MLIRPythonNCompile.dialects.gen
  ROOT_DIR "${CMAKE_CURRENT_BINARY_DIR}/ncompile"
  ADD_TO_PARENT MLIRPythonNCompile.sources
  SOURCES
    dialects/_qec_ops_gen.py
)
add_dependencies(MLIRPythonNCompile.dialects.gen MLIRPythonQEC.tablegen)

# Declare the C++ extension module
declare_mlir_python_extension(MLIRPythonNCompile.extension
  MODULE_NAME _ncompileDialectsQEC
  ADD_TO_PARENT MLIRPythonNCompile.sources
  SOURCES
    QECModule.cpp
    ../lib/CAPI/Dialect/QEC/QEC.cpp
  PRIVATE_LINK_LIBS
    MLIRQECDialect
    MLIRCAPIIR
    MLIRIR
)

# Finalize the Python modules
add_mlir_python_modules(MLIRPythonNCompile
  ROOT_PREFIX "${CMAKE_CURRENT_BINARY_DIR}/python_packages/ncompile"
  INSTALL_PREFIX "python_packages/ncompile"
  DECLARED_SOURCES
    MLIRPythonNCompile.sources
)
