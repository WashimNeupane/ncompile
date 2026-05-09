#ifndef NCOMPILE_TRANSFORMS_PASSES
#define NCOMPILE_TRANSFORMS_PASSES

include "mlir/Pass/PassBase.td"

def QECSchedule : Pass<"qec-schedule", "mlir::ModuleOp"> {
  let summary = "Schedule QEC measurements into non-conflicting time slices";
  let description = [{
    This pass analyzes the dependencies between measure_pauli operations
    and groups them into discrete time slices to minimize total circuit depth.
  }];
  let constructor = "mlir::ncompile::createQECSchedulePass()";
  let dependentDialects = ["mlir::qec::QECDialect"];
  let options = [
    Option<"naive", "naive", "bool", "false", "Assign each op to a unique time slice (serial)">
  ];
}

#endif // NCOMPILE_TRANSFORMS_PASSES
