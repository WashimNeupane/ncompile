"""
@file gen_gross_code.py
@brief Two-round simulation generator with resets for Bivariate Bicycle codes.
@author Washim Neupane (washimneupane@outlook.com)
"""

import sys
from mlir.ir import *
from ncompile.dialects import qec

@register_attribute_builder("QEC_CodeType")
def _qecCodeType(x, context):
    return IntegerAttr.get(IntegerType.get_signless(32, context=context), x)

def gen_gross_code(L=6):
    ctx = Context()
    qec.register_dialect(ctx)

    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            qubit_types = [qec.Qubit.get(ctx, layer, i) for layer in range(2) for i in range(L*L)]
            all_qubits = list(qec.initialize(qubit_types, 1, L))

            # Reset all qubits to |0>
            for q in all_qubits:
                qec.reset(q)

            syndrome_type = qec.Syndrome.get(ctx)
            px_val = qec.pauli_str(qec.Pauli.get("XXXXXX", ctx), "XXXXXX")
            pz_val = qec.pauli_str(qec.Pauli.get("ZZZZZZ", ctx), "ZZZZZZ")

            def idx(layer, r, c):
                return layer * (L*L) + (r % L) * L + (c % L)

            # --- ROUND 0 (Reference) ---
            round0_syndromes = []
            # X-checks
            for r in range(L):
                for c in range(L):
                    q_a = [all_qubits[idx(0, r + 3, c)], all_qubits[idx(0, r, c + 1)], all_qubits[idx(0, r, c + 2)]]
                    q_b = [all_qubits[idx(1, r, c + 3)], all_qubits[idx(1, r + 1, c)], all_qubits[idx(1, r + 2, c)]]
                    s = qec.measure_pauli(syndrome_type, q_a + q_b, px_val)
                    round0_syndromes.append(s)

            # Z-checks
            for r in range(L):
                for c in range(L):
                    q_bt = [all_qubits[idx(0, r, c + 3)], all_qubits[idx(0, r + 5, c)], all_qubits[idx(0, r + 4, c)]]
                    q_at = [all_qubits[idx(1, r + 3, c)], all_qubits[idx(1, r, c + 5)], all_qubits[idx(1, r, c + 4)]]
                    s = qec.measure_pauli(syndrome_type, q_bt + q_at, pz_val)
                    round0_syndromes.append(s)

            # --- ROUND 1 (Noisy) ---
            round1_syndromes = []
            # X-checks
            for r in range(L):
                for c in range(L):
                    q_a = [all_qubits[idx(0, r + 3, c)], all_qubits[idx(0, r, c + 1)], all_qubits[idx(0, r, c + 2)]]
                    q_b = [all_qubits[idx(1, r, c + 3)], all_qubits[idx(1, r + 1, c)], all_qubits[idx(1, r + 2, c)]]
                    s = qec.measure_pauli(syndrome_type, q_a + q_b, px_val)
                    round1_syndromes.append(s)

            # Z-checks
            for r in range(L):
                for c in range(L):
                    q_bt = [all_qubits[idx(0, r, c + 3)], all_qubits[idx(0, r + 5, c)], all_qubits[idx(0, r + 4, c)]]
                    q_at = [all_qubits[idx(1, r + 3, c)], all_qubits[idx(1, r, c + 5)], all_qubits[idx(1, r, c + 4)]]
                    s = qec.measure_pauli(syndrome_type, q_bt + q_at, pz_val)
                    round1_syndromes.append(s)

            # --- DETECTORS (Compare Round 0 and Round 1) ---
            for i in range(len(round0_syndromes)):
                qec.detector([round0_syndromes[i], round1_syndromes[i]])

            # --- LOGICAL OBSERVABLE ---
            qec.logical_observable(syndrome=syndrome_type, targets=[round1_syndromes[0]])

        print(module)

if __name__ == "__main__":
    L_val = 6
    if len(sys.argv) > 1:
        L_val = int(sys.argv[1])
    gen_gross_code(L_val)
