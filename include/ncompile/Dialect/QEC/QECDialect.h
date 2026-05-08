#ifndef QEC_DIALECT_H
#define QEC_DIALECT_H

#include "mlir/Bytecode/BytecodeImplementation.h"
#include "mlir/Bytecode/BytecodeOpInterface.h"
#include "mlir/IR/Builders.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"

#include "ncompile/Dialect/QEC/QECDialect.h.inc"

#define GET_OP_CLASSES
#include "ncompile/Dialect/QEC/QECOps.h.inc"

#define GET_TYPEDEF_CLASSES
#include "ncompile/Dialect/QEC/QECDialectTypes.h.inc"

#endif // QEC_DIALECT_H
