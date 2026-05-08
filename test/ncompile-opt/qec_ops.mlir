// RUN: qeccc-opt %s | FileCheck %s

// CHECK-LABEL: @qec_valid
func.func @qec_valid() {
  // CHECK: %{{.*}} = qec.patch_config "surface", 3 : <"surface", 3>
  %config_val = qec.patch_config "surface", 3 : !qec.patch<"surface", 3>

  // CHECK: %{{.*}}:4 = qec.initialize "surface", 3 -> !qec.qubit, !qec.qubit, !qec.qubit, !qec.qubit
  %q:4 = qec.initialize "surface", 3 -> !qec.qubit, !qec.qubit, !qec.qubit, !qec.qubit

  // CHECK: %{{.*}} = qec.pauli_str "XXYY" : <"XXYY">
  %pauli = qec.pauli_str "XXYY" : !qec.pauli<"XXYY">

  // CHECK: %{{.*}} = qec.measure_pauli(%{{.*}}#0, %{{.*}}#1, %{{.*}}#2, %{{.*}}#3), %{{.*}} : (!qec.qubit, !qec.qubit, !qec.qubit, !qec.qubit), <"XXYY"> -> !qec.syndrome
  %syndrome = qec.measure_pauli(%q#0, %q#1, %q#2, %q#3), %pauli : (!qec.qubit, !qec.qubit, !qec.qubit, !qec.qubit), !qec.pauli<"XXYY"> -> !qec.syndrome

  // CHECK: qec.detector(%{{.*}}) : (!qec.syndrome)
  qec.detector(%syndrome) : (!qec.syndrome)

  // CHECK: %{{.*}} = qec.logical_observable(%{{.*}}) : (!qec.syndrome) -> !qec.syndrome
  %obs = qec.logical_observable(%syndrome) : (!qec.syndrome) -> !qec.syndrome

  // Low-level ops
  // CHECK: qec.cx %{{.*}}#0, %{{.*}}#1 : !qec.qubit, !qec.qubit
  qec.cx %q#0, %q#1 : !qec.qubit, !qec.qubit

  // CHECK: qec.reset %{{.*}}#0 : !qec.qubit
  qec.reset %q#0 : !qec.qubit

  // CHECK: %{{.*}} = qec.measure %{{.*}}#0 : !qec.qubit -> !qec.syndrome
  %s2 = qec.measure %q#0 : !qec.qubit -> !qec.syndrome

  // CHECK: qec.idle %{{.*}}#0 : !qec.qubit
  qec.idle %q#0 : !qec.qubit

  return
}
