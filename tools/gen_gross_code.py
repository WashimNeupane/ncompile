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
    """Generates the MLIR IR for the Gross code benchmark."""
    ctx = Context()
    qec.register_dialect(ctx)

    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            # QEC_CodeType: BivariateBicycle = 1
            # distance = 6
            qubit_types = [qec.Qubit.get(ctx, i, j) for i in range(6) for j in range(12)]

            # Using the manually registered builder
            init_op = qec.initialize(qubit_types, 1, 6)

            all_qubits = list(init_op)

            pauli_x = qec.Pauli.get("X", ctx)
            pauli_z = qec.Pauli.get("Z", ctx)

            # Pauli values via PauliStrOp
            p_x_val = qec.pauli_str(qec.Pauli.get("X", ctx), "X")
            p_z_val = qec.pauli_str(qec.Pauli.get("Z", ctx), "Z")

            syndrome_type = qec.Syndrome.get(ctx)

            # Create some measure_pauli ops
            qec.measure_pauli(syndrome_type, all_qubits[:6], p_x_val)
            qec.measure_pauli(syndrome_type, all_qubits[6:12], p_z_val)

        print(module)

if __name__ == "__main__":
    gen_gross_code()
