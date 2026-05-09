// RUN: qeccc-opt %s -split-input-file -verify-diagnostics

func.func @invalid_pauli() {
  %pauli = qec.pauli_str "XYZH" : !qec.pauli<"XYZH"> // expected-error {{invalid character in Pauli string: 'H'}}
  return
}

// -----

func.func @invalid_distance() {
  %q:4 = qec.initialize Surface, -1 -> !qec.qubit<0,0>, !qec.qubit<0,1>, !qec.qubit<1,0>, !qec.qubit<1,1> // expected-error {{distance must be a positive integer, got -1}}
  return
}

// -----

func.func @mismatched_pauli_length(%q0: !qec.qubit<0,0>, %q1: !qec.qubit<0,1>) {
  %pauli = qec.pauli_str "XYZ" : !qec.pauli<"XYZ">
  %syndrome = qec.measure_pauli(%q0, %q1), %pauli : (!qec.qubit<0,0>, !qec.qubit<0,1>), !qec.pauli<"XYZ"> -> !qec.syndrome // expected-error {{Pauli string length (3) does not match number of qubits (2)}}
  return
}

// -----

func.func @cx_same_qubit(%q: !qec.qubit<0,0>) {
  qec.cx %q, %q : !qec.qubit<0,0>, !qec.qubit<0,0> // expected-error {{control and target qubits must be different}}
  return
}
