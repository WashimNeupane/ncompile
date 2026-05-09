#ifndef NCOMPILE_C_DIALECT_QEC_H
#define NCOMPILE_C_DIALECT_QEC_H

#include "mlir-c/IR.h"
#include "mlir-c/Support.h"

#ifdef __cplusplus
extern "C" {
#endif

MLIR_DECLARE_CAPI_DIALECT_REGISTRATION(QEC, qec);

//===----------------------------------------------------------------------===//
// QEC Type check/creation
//===----------------------------------------------------------------------===//

MLIR_CAPI_EXPORTED bool ncompileMlirTypeIsAQECQubit(MlirType type);
MLIR_CAPI_EXPORTED MlirType ncompileMlirQECQubitTypeGet(MlirContext ctx,
                                                        int64_t x, int64_t y);

MLIR_CAPI_EXPORTED bool ncompileMlirTypeIsAQECSyndrome(MlirType type);
MLIR_CAPI_EXPORTED MlirType ncompileMlirQECSyndromeTypeGet(MlirContext ctx);

MLIR_CAPI_EXPORTED bool ncompileMlirTypeIsAQECPauli(MlirType type);
MLIR_CAPI_EXPORTED MlirType
ncompileMlirQECPauliTypeGet(MlirContext ctx, MlirStringRef pauliString);

#ifdef __cplusplus
}
#endif

#endif // NCOMPILE_C_DIALECT_QEC_H
