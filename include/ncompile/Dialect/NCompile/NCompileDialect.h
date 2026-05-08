#ifndef NCOMPILE_DIALECT_H
#define NCOMPILE_DIALECT_H

#include "mlir/IR/Dialect.h"
#include "mlir/IR/OpDefinition.h"

#include "ncompile/Dialect/NCompile/NCompileDialect.h.inc"

#define GET_OP_CLASSES
#include "ncompile/Dialect/NCompile/NCompileOps.h.inc"

#endif // NCOMPILE_DIALECT_H
