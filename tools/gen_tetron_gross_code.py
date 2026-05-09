import sys
from mlir.ir import *
from ncompile.dialects import qec

@register_attribute_builder("QEC_CodeType")
def _qecCodeType(x, context):
    return IntegerAttr.get(IntegerType.get_signless(32, context=context), x)

def gen_tetron_gross_code(L=6):
    ctx = Context()
    qec.register_dialect(ctx)

    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            # Each logical qubit is a Tetron (4 MZMs)
            # Total logical qubits: 2 * L * L
            # Total MZMs: 8 * L * L

            # Map logical index (layer, r, c) to Tetron base (R, C)
            # Use spacing of 2 to leave "Ancilla Highways"
            def get_tetron_base(layer, r, c):
                # layer 0 on top, layer 1 on bottom
                # spacing = 2 means every other row/col is empty
                return ((layer * L + r) * 2, c * 2)

            # Initialize MZMs
            mzm_types = []
            for layer in range(2):
                for r in range(L):
                    for c in range(L):
                        tR, tC = get_tetron_base(layer, r, c)
                        # 4 MZMs per tetron
                        mzm_types.append(qec.MZM.get(ctx, 2*tR, 2*tC))
                        mzm_types.append(qec.MZM.get(ctx, 2*tR, 2*tC+1))
                        mzm_types.append(qec.MZM.get(ctx, 2*tR+1, 2*tC))
                        mzm_types.append(qec.MZM.get(ctx, 2*tR+1, 2*tC+1))

            all_mzms = list(qec.mzm_init(mzm_types))

            def get_mzm(layer, r, c, m_idx):
                base = (layer * (L*L) + r * L + c) * 4
                return all_mzms[base + m_idx]

            syndrome_type = qec.Syndrome.get(ctx)

            # In the Tetron model, a Pauli-X on logical qubit i is a parity measurement
            # between MZM 0 and 1. Pauli-Z is MZM 0 and 2.
            # (Simplification for the project)

            # X-checks
            for r in range(L):
                for c in range(L):
                    # Logical parity XXXXXX is a joint parity of 12 MZMs (2 per tetron)
                    targets = []
                    q_indices = [
                        (0, (r + 3) % L, c), (0, r, (c + 1) % L), (0, r, (c + 2) % L),
                        (1, r, (c + 3) % L), (1, (r + 1) % L, c), (1, (r + 2) % L, c)
                    ]
                    for layer, qr, qc in q_indices:
                        targets.append(get_mzm(layer, qr, qc, 0))
                        targets.append(get_mzm(layer, qr, qc, 1))

                    qec.measure_parity(syndrome_type, targets)

            # Z-checks
            for r in range(L):
                for c in range(L):
                    targets = []
                    q_indices = [
                        (0, r, (c + 3) % L), (0, (r + 5) % L, c), (0, (r + 4) % L, c),
                        (1, (r + 3) % L, c), (1, r, (c + 5) % L), (1, (r + 4) % L, c)
                    ]
                    for layer, qr, qc in q_indices:
                        targets.append(get_mzm(layer, qr, qc, 0))
                        targets.append(get_mzm(layer, qr, qc, 2))

                    qec.measure_parity(syndrome_type, targets)

        print(module)

if __name__ == "__main__":
    gen_tetron_gross_code()
