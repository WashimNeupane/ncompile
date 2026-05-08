#ifndef NCOMPILE_DIALECT_NCOMPILE_NCOMPILEDIALECT_H
#define NCOMPILE_DIALECT_NCOMPILE_NCOMPILEDIALECT_H

#include "mlir/Bytecode/BytecodeImplementation.h"
#include "mlir/Bytecode/BytecodeOpInterface.h"
#include "mlir/IR/Builders.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"

#include "ncompile/Dialect/NCompile/NCompileDialect.h.inc"

#define GET_OP_CLASSES
#include "ncompile/Dialect/NCompile/NCompileOps.h.inc"

#endif // NCOMPILE_DIALECT_NCOMPILE_NCOMPILEDIALECT_H
