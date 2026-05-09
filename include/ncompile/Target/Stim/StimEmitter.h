#ifndef NCOMPILE_TARGET_STIM_STIMEMITTER_H
#define NCOMPILE_TARGET_STIM_STIMEMITTER_H

#include "mlir/Support/LLVM.h"
#include "llvm/Support/raw_ostream.h"

namespace mlir {
class ModuleOp;

namespace qec {

/// Translates the given QEC module to Stim circuit format.
LogicalResult translateToStim(ModuleOp module, raw_ostream& output,
                              double errorRate = 0.0);

} // namespace qec
} // namespace mlir

#endif // NCOMPILE_TARGET_STIM_STIMEMITTER_H
