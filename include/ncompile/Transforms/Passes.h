#ifndef NCOMPILE_TRANSFORMS_PASSES_H
#define NCOMPILE_TRANSFORMS_PASSES_H

#include "mlir/Pass/Pass.h"
#include <memory>

namespace mlir {
class ModuleOp;

namespace ncompile {

std::unique_ptr<Pass> createQECSchedulePass();

#define GEN_PASS_REGISTRATION
#include "ncompile/Transforms/Passes.h.inc"

} // namespace ncompile
} // namespace mlir

#endif // NCOMPILE_TRANSFORMS_PASSES_H
