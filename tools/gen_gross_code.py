"""
@file gen_gross_code.py
@brief Benchmark generator for the [[72, 12, 6]] Gross code.
@author Washim Neupane (washimneupane@outlook.com)

This script uses the ncompile QEC dialect to generate a high-level MLIR
representation of the Bivariate Bicycle code (Gross code).
"""

from mlir.ir import *
from ncompile.dialects import qec

@register_attribute_builder("QEC_CodeType")
def _qecCodeType(x, context):
    """Builder for the QEC_CodeType enum attribute."""
    return IntegerAttr.get(IntegerType.get_signless(32, context=context), x)

def gen_gross_code():
    """Generates the MLIR IR for the Gross code benchmark [[72, 12, 6]]."""
    ctx = Context()
    # Explicitly register and load the dialect to enable custom assembly format (pretty-printing)
    qec.register_dialect(ctx)

    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            # 72 physical qubits in two 6x6 layers
            # Layer 1: 0-35, Layer 2: 36-71
            qubit_types = [qec.Qubit.get(ctx, layer, i) for layer in range(2) for i in range(36)]

            # Initialize the code (BivariateBicycle = 1)
            # The initialize op returns a variadic result (list of values)
            all_qubits = list(qec.initialize(qubit_types, 1, 6))

            # Common syndrome type
            syndrome_type = qec.Syndrome.get(ctx)

            # Parity checks are weight 6
            pauli_x6 = qec.Pauli.get("XXXXXX", ctx)
            pauli_z6 = qec.Pauli.get("ZZZZZZ", ctx)

            px_val = qec.pauli_str(pauli_x6, "XXXXXX")
            pz_val = qec.pauli_str(pauli_z6, "ZZZZZZ")

            # Helper to get index in Layer 1/2 from (r, c)
            def idx(layer, r, c):
                return layer * 36 + (r % 6) * 6 + (c % 6)

            # Generate 36 X-checks from Hx = [A | B]
            # A = x^3 + y^1 + y^2
            # B = y^3 + x^1 + x^2
            for r in range(6):
                for c in range(6):
                    # Check qubits in Layer 1 (Block A)
                    q_a = [
                        all_qubits[idx(0, r + 3, c)],
                        all_qubits[idx(0, r, c + 1)],
                        all_qubits[idx(0, r, c + 2)]
                    ]
                    # Check qubits in Layer 2 (Block B)
                    q_b = [
                        all_qubits[idx(1, r, c + 3)],
                        all_qubits[idx(1, r + 1, c)],
                        all_qubits[idx(1, r + 2, c)]
                    ]
                    qec.measure_pauli(syndrome_type, q_a + q_b, px_val)

            # Generate 36 Z-checks from Hz = [B^T | A^T]
            # B^T = y^3 + x^5 + x^4 (since x^-1 = x^5)
            # A^T = x^3 + y^5 + y^4
            for r in range(6):
                for c in range(6):
                    # Check qubits in Layer 1 (Block B^T)
                    q_bt = [
                        all_qubits[idx(0, r, c + 3)],
                        all_qubits[idx(0, r + 5, c)],
                        all_qubits[idx(0, r + 4, c)]
                    ]
                    # Check qubits in Layer 2 (Block A^T)
                    q_at = [
                        all_qubits[idx(1, r + 3, c)],
                        all_qubits[idx(1, r, c + 5)],
                        all_qubits[idx(1, r, c + 4)]
                    ]
                    qec.measure_pauli(syndrome_type, q_bt + q_at, pz_val)

        # Print using the pretty format
        print(module)

if __name__ == "__main__":
    gen_gross_code()
