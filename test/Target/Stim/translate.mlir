// RUN: qeccc-translate --qec-to-stim %s | FileCheck %s

func.func @test_stim_translation() {
  // CHECK-DAG: QUBIT_COORDS(0, 0) 0
  // CHECK-DAG: QUBIT_COORDS(1, 1) 1
  %q0 = qec.initialize Surface, 3 -> !qec.qubit<0, 0>
  %q1 = qec.initialize Surface, 3 -> !qec.qubit<1, 1>

  // CHECK: MPP X0 Z1
  %p = qec.pauli_str "XZ" : !qec.pauli<"XZ">
  %s_pauli = qec.measure_pauli(%q0, %q1), %p : (!qec.qubit<0, 0>, !qec.qubit<1, 1>), !qec.pauli<"XZ"> -> !qec.syndrome

  // CHECK: R 0
  qec.reset %q0 : !qec.qubit<0, 0>

  // CHECK: CNOT 0 1
  qec.cx %q0, %q1 : !qec.qubit<0, 0>, !qec.qubit<1, 1>

  // CHECK: M 1
  %s_m = qec.measure %q1 : !qec.qubit<1, 1> -> !qec.syndrome

  // CHECK: DETECTOR rec[-2] rec[-1]
  qec.detector(%s_pauli, %s_m) : (!qec.syndrome, !qec.syndrome)

  // CHECK: OBSERVABLE_INCLUDE(0) rec[-1]
  %obs = qec.logical_observable(%s_m) : (!qec.syndrome) -> !qec.syndrome

  // CHECK: TICK
  qec.idle %q0 : !qec.qubit<0, 0>

  return
}
