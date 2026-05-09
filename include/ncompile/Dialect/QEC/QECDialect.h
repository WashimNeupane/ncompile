/**
 * @file QECDialect.h
 * @brief Main header for the QEC Dialect.
 *
 * @ingroup qec_dialect
 */

#ifndef QEC_DIALECT_H
#define QEC_DIALECT_H

#include "mlir/Bytecode/BytecodeOpInterface.h"
#include "mlir/IR/Builders.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/IR/OpImplementation.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"

#include "ncompile/Dialect/QEC/QECDialect.h.inc"

#include "ncompile/Dialect/QEC/QECDialectEnums.h.inc"

#define GET_TYPEDEF_CLASSES
#include "ncompile/Dialect/QEC/QECDialectTypes.h.inc"

#define GET_OP_CLASSES
#include "ncompile/Dialect/QEC/QECOps.h.inc"

#endif // QEC_DIALECT_H
