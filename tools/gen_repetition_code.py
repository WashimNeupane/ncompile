import sys
from mlir.ir import *
from ncompile.dialects import qec

@register_attribute_builder("QEC_CodeType")
def _qecCodeType(x, context):
    return IntegerAttr.get(IntegerType.get_signless(32, context=context), x)

def gen_repetition_code(d=5):
    ctx = Context()
    qec.register_dialect(ctx)
    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            qubit_types = [qec.Qubit.get(ctx, 0, i) for i in range(d)]
            qubits = list(qec.initialize(qubit_types, 1, d))

            syndrome_type = qec.Syndrome.get(ctx)
            pz2 = qec.pauli_str(qec.Pauli.get("ZZ", ctx), "ZZ")

            def emit_round():
                syns = []
                for i in range(d-1):
                    syns.append(qec.measure_pauli(syndrome_type, [qubits[i], qubits[i+1]], pz2))
                return syns

            r0 = emit_round()
            r1 = emit_round()
            for i in range(len(r0)):
                qec.detector([r0[i], r1[i]])

            qec.logical_observable(syndrome=syndrome_type, targets=[r1[0]])

        print(module)

if __name__ == "__main__":
    gen_repetition_code()
