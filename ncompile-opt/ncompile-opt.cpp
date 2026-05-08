#include "mlir/IR/Dialect.h"
#include "mlir/IR/MLIRContext.h"
#include "mlir/InitAllDialects.h"
#include "mlir/InitAllPasses.h"
#include "mlir/Tools/mlir-opt/MlirOptMain.h"
#include "ncompile/Dialect/NCompile/NCompileDialect.h"

int main(int argc, char **argv) {
  mlir::DialectRegistry registry;
  mlir::registerAllDialects(registry);
  mlir::registerAllPasses();

  registry.insert<mlir::ncompile::NCompileDialect>();

  return mlir::asMainReturnCode(
      mlir::MlirOptMain(argc, argv, "NCompile optimizer driver\n", registry));
}
