import sys
from mlir.ir import *
from ncompile.dialects import qec

def gen_tetron_repetition_code(d=3, rounds=3):
    ctx = Context()
    qec.register_dialect(ctx)

    with ctx, Location.unknown():
        module = Module.create()
        with InsertionPoint(module.body):
            # Initialize a dense grid of MZMs to allow highways
            mzm_types = []
            grid_height = d * 4
            for r in range(grid_height):
                for c in range(2):
                    mzm_types.append(qec.MZM.get(ctx, r, c))

            all_mzms = list(qec.mzm_init(mzm_types))

            def get_mzm(r, c):
                return all_mzms[r * 2 + c]

            syndrome_type = qec.Syndrome.get(ctx)

            syndromes = []
            for r in range(rounds):
                # Repetition checks: parity between logical qubit i and i+1
                # Logical qubit i is at row 4*i
                for i in range(d - 1):
                    targets = []
                    # Path from row 4*i to 4*(i+1)
                    for row in range(4*i, 4*(i+1) + 1):
                        targets.append(get_mzm(row, 0))

                    res = qec.measure_parity(syndrome_type, targets)
                    syndromes.append(res)
                    if r > 0:
                        prev_res = syndromes[(r-1) * (d-1) + i]
                        qec.detector([res, prev_res])
                    else:
                        qec.detector([res])

            # Observable (Logical X is parity of data MZMs at start and end)
            obs_targets = []
            for row in range(0, (d-1)*4 + 1):
                obs_targets.append(get_mzm(row, 1))
            obs_res = qec.measure_parity(syndrome_type, obs_targets)
            qec.logical_observable(syndrome_type, [obs_res])

        print(module)

if __name__ == "__main__":
    gen_tetron_repetition_code()
