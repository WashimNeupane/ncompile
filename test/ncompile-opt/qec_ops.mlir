// RUN: qeccc-opt %s | FileCheck %s

// CHECK-LABEL: @qec_valid
func.func @qec_valid() {
  // CHECK: %{{.*}} = qec.patch_config "surface", 3 : <"surface", 3>
  %config_val = qec.patch_config "surface", 3 : !qec.patch<"surface", 3>

  // CHECK: %{{.*}}:4 = qec.initialize Surface, 3 -> !qec.qubit<0, 0>, !qec.qubit<0, 1>, !qec.qubit<1, 0>, !qec.qubit<1, 1>
  %q:4 = qec.initialize Surface, 3 -> !qec.qubit<0, 0>, !qec.qubit<0, 1>, !qec.qubit<1, 0>, !qec.qubit<1, 1>

  // CHECK: %{{.*}} = qec.pauli_str "XXYY" : <"XXYY">
  %pauli = qec.pauli_str "XXYY" : !qec.pauli<"XXYY">

  // CHECK: %{{.*}} = qec.measure_pauli(%{{.*}}#0, %{{.*}}#1, %{{.*}}#2, %{{.*}}#3), %{{.*}} : (!qec.qubit<0, 0>, !qec.qubit<0, 1>, !qec.qubit<1, 0>, !qec.qubit<1, 1>), <"XXYY"> -> !qec.syndrome
  %syndrome = qec.measure_pauli(%q#0, %q#1, %q#2, %q#3), %pauli : (!qec.qubit<0, 0>, !qec.qubit<0, 1>, !qec.qubit<1, 0>, !qec.qubit<1, 1>), !qec.pauli<"XXYY"> -> !qec.syndrome

  // CHECK: qec.detector(%{{.*}}) : (!qec.syndrome)
  qec.detector(%syndrome) : (!qec.syndrome)

  // CHECK: %{{.*}} = qec.logical_observable(%{{.*}}) : (!qec.syndrome) -> !qec.syndrome
  %obs = qec.logical_observable(%syndrome) : (!qec.syndrome) -> !qec.syndrome

  // Low-level ops
  // CHECK: qec.cx %{{.*}}#0, %{{.*}}#1 : <0, 0>, <0, 1>
  qec.cx %q#0, %q#1 : !qec.qubit<0, 0>, !qec.qubit<0, 1>

  // CHECK: qec.reset %{{.*}}#0 : <0, 0>
  qec.reset %q#0 : !qec.qubit<0, 0>

  // CHECK: %{{.*}} = qec.measure %{{.*}}#0 : <0, 0> -> !qec.syndrome
  %s2 = qec.measure %q#0 : !qec.qubit<0, 0> -> !qec.syndrome

  // CHECK: qec.idle %{{.*}}#0 : <0, 0>
  qec.idle %q#0 : !qec.qubit<0, 0>

  return
}
