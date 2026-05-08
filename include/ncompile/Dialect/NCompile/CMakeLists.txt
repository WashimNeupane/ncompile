set(LLVM_TARGET_DEFINITIONS NCompileDialect.td)
mlir_tablegen(NCompileDialect.h.inc -gen-dialect-decls -dialect=ncompile)
mlir_tablegen(NCompileDialect.cpp.inc -gen-dialect-defs -dialect=ncompile)
add_public_tablegen_target(NCompileDialectIncGen)

set(LLVM_TARGET_DEFINITIONS NCompileOps.td)
mlir_tablegen(NCompileOps.h.inc -gen-op-decls)
mlir_tablegen(NCompileOps.cpp.inc -gen-op-defs)
add_public_tablegen_target(NCompileOpsIncGen)
