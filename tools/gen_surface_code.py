import sys
from mlir.ir import *
from ncompile.dialects import qec

@register_attribute_builder("QEC_CodeType")
def _qecCodeType(x, context):
    return IntegerAttr.get(IntegerType.get_signless(32, context=context), x)

def gen_surface_code(d=3):
    ctx = Context()
    qec.register_dialect(ctx)
    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            n = d*d
            qubit_types = [qec.Qubit.get(ctx, 0, i) for i in range(n)]
            qubits = list(qec.initialize(qubit_types, 1, d))

            syndrome_type = qec.Syndrome.get(ctx)
            px2 = qec.pauli_str(qec.Pauli.get("XX", ctx), "XX")
            px4 = qec.pauli_str(qec.Pauli.get("XXXX", ctx), "XXXX")
            pz2 = qec.pauli_str(qec.Pauli.get("ZZ", ctx), "ZZ")
            pz4 = qec.pauli_str(qec.Pauli.get("ZZZZ", ctx), "ZZZZ")

            def get_q(r, c): return qubits[r*d + c]

            # rounds
            def emit_round():
                syns = []
                # X-checks
                for r in range(d-1):
                    for c in range(d-1):
                        if (r+c) % 2 == 1:
                            qs = [get_q(r,c), get_q(r+1,c), get_q(r,c+1), get_q(r+1,c+1)]
                            syns.append(qec.measure_pauli(syndrome_type, qs, px4))
                # Z-checks
                for r in range(d-1):
                    for c in range(d-1):
                        if (r+c) % 2 == 0:
                            qs = [get_q(r,c), get_q(r+1,c), get_q(r,c+1), get_q(r+1,c+1)]
                            syns.append(qec.measure_pauli(syndrome_type, qs, pz4))
                return syns

            r0 = emit_round()
            r1 = emit_round()
            for i in range(len(r0)):
                qec.detector([r0[i], r1[i]])

            qec.logical_observable(syndrome=syndrome_type, targets=[r1[0]])

        print(module)

if __name__ == "__main__":
    gen_surface_code()
