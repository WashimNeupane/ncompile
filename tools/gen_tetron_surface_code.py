import sys

def gen_surface(d, p_noise):
    print("module {")
    # Rotated Surface Code dxd
    # Qubits: (2d-1) x (2d-1) grid of potential MZM sites
    # Data qubits: d^2
    # Ancilla checks: d^2 - 1

    # Simple layout:
    # Data MZMs at (2i, 2j) for i,j in range(d)
    # Actually, each "qubit" in Tetron is 4 MZMs.
    # To keep it simple, let's just use 1 MZM per site and weight-4 checks.

    mzm_count = (2*d+1) * (2*d+1)
    mzm_types = ", ".join([f"!qec.mzm<{i % (2*d+1)}, {i // (2*d+1)}>" for i in range(mzm_count)])
    print(f"  %mzms:{mzm_count} = qec.mzm_init -> ({mzm_types})")

    def get_id(x, y):
        return y * (2*d+1) + x

    syndromes = []
    # Parity checks (Alternating X and Z)
    for r in range(d):
        print(f"  // Round {r}")
        current_round_syndromes = []
        for x in range(1, 2*d, 2):
            for y in range(1, 2*d, 2):
                # Weight-4 check around (x, y)
                m1 = get_id(x-1, y-1)
                m2 = get_id(x+1, y-1)
                m3 = get_id(x-1, y+1)
                m4 = get_id(x+1, y+1)
                s_name = f"s{r}_{x}_{y}"
                print(f"  %{s_name} = qec.measure_parity %mzms#{m1}, %mzms#{m2}, %mzms#{m3}, %mzms#{m4} {{noise = {p_noise}}} : (!qec.mzm<{x-1}, {y-1}>, !qec.mzm<{x+1}, {y-1}>, !qec.mzm<{x-1}, {y+1}>, !qec.mzm<{x+1}, {y+1}>) -> !qec.syndrome")
                current_round_syndromes.append((x, y, f"%{s_name}"))

        # Detectors
        if r > 0:
            for i, (x, y, s) in enumerate(current_round_syndromes):
                prev_s = f"%s{r-1}_{x}_{y}"
                print(f"  qec.detector({s}, {prev_s}) : (!qec.syndrome, !qec.syndrome)")

        syndromes.append(current_round_syndromes)

    # Logical Observable (Boundary to boundary)
    log_targets = [s for x, y, s in syndromes[-1] if x == 1]
    args = ", ".join(log_targets)
    types = ", ".join(["!qec.syndrome"] * len(log_targets))
    print(f"  %log = qec.logical_observable({args}) : ({types}) -> !qec.syndrome")

    print("}")

if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    p = float(sys.argv[2]) if len(sys.argv) > 2 else 0.001
    gen_surface(d, p)
