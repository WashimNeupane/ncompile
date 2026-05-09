/**
 * @file QEC.h
 * @brief C-API for the QEC Dialect.
 *
 * This file provides the C-API hooks for the QEC dialect, allowing
 * interoperability with Python and other languages.
 *
 * @ingroup qec_capi
 */

#ifndef NCOMPILE_C_DIALECT_QEC_H
#define NCOMPILE_C_DIALECT_QEC_H

#include "mlir-c/IR.h"
#include "mlir-c/Support.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Registers the QEC dialect in the provided registry.
 */
MLIR_DECLARE_CAPI_DIALECT_REGISTRATION(QEC, qec);

//===----------------------------------------------------------------------===//
// QEC Type check/creation
//===----------------------------------------------------------------------===//

/**
 * @brief Returns true if the given type is a QEC Qubit type.
 */
MLIR_CAPI_EXPORTED bool ncompileMlirTypeIsAQECQubit(MlirType type);

/**
 * @brief Creates a QEC Qubit type with coordinates (x, y).
 */
MLIR_CAPI_EXPORTED MlirType ncompileMlirQECQubitTypeGet(MlirContext ctx,
                                                        int64_t x, int64_t y);

/**
 * @brief Returns true if the given type is a QEC Syndrome type.
 */
MLIR_CAPI_EXPORTED bool ncompileMlirTypeIsAQECSyndrome(MlirType type);

/**
 * @brief Creates a QEC Syndrome type.
 */
MLIR_CAPI_EXPORTED MlirType ncompileMlirQECSyndromeTypeGet(MlirContext ctx);

/**
 * @brief Returns true if the given type is a QEC Pauli type.
 */
MLIR_CAPI_EXPORTED bool ncompileMlirTypeIsAQECPauli(MlirType type);

/**
 * @brief Creates a QEC Pauli type from a string (e.g., "X", "Z", "I").
 */
MLIR_CAPI_EXPORTED MlirType
ncompileMlirQECPauliTypeGet(MlirContext ctx, MlirStringRef pauliString);

#ifdef __cplusplus
}
#endif

#endif // NCOMPILE_C_DIALECT_QEC_H
