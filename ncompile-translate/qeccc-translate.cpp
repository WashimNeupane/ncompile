#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/IR/BuiltinOps.h"
#include "mlir/InitAllDialects.h"
#include "mlir/Support/LogicalResult.h"
#include "mlir/Tools/mlir-translate/MlirTranslateMain.h"
#include "mlir/Tools/mlir-translate/Translation.h"
#include "ncompile/Dialect/QEC/QECDialect.h"
#include "ncompile/Target/Stim/StimEmitter.h"

using namespace mlir;

namespace mlir {
void registerStimTranslation() {
  TranslateFromMLIRRegistration registration(
      "qec-to-stim", "translate from qec to stim",
      [](ModuleOp module, raw_ostream& output) {
        return qec::translateToStim(module, output);
      },
      [](DialectRegistry& registry) {
        registry.insert<qec::QECDialect, func::FuncDialect>();
      });
}
} // namespace mlir

int main(int argc, char** argv) {
  DialectRegistry registry;
  registerAllDialects(registry);
  registry.insert<qec::QECDialect, func::FuncDialect>();

  // Register our custom translation
  mlir::registerStimTranslation();

  return failed(mlirTranslateMain(argc, argv, "QEC Translator tool"));
}
