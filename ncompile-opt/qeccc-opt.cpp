#include "mlir/IR/MLIRContext.h"
#include "mlir/InitAllDialects.h"
#include "mlir/InitAllPasses.h"
#include "mlir/Support/FileUtilities.h"
#include "mlir/Tools/mlir-opt/MlirOptMain.h"

#include "ncompile/Dialect/QEC/QECDialect.h"
#include "ncompile/Transforms/Passes.h"

int main(int argc, char** argv) {
  mlir::registerAllPasses();
  mlir::ncompile::registerNCompilePasses();

  mlir::DialectRegistry registry;
  mlir::registerAllDialects(registry);
  registry.insert<mlir::qec::QECDialect>();

  return mlir::asMainReturnCode(
      mlir::MlirOptMain(argc, argv, "qeccc-opt Optimizer Driver\n", registry));
}
