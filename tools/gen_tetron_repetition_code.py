import sys

def gen_repetition(d, noise):
    print("module {")
    mzm_types = ", ".join([f"!qec.mzm<{i}, 0>" for i in range(2 * d)])
    print(f"  %mzms:{2*d} = qec.mzm_init -> ({mzm_types})")

    for r in range(d):
        print(f"  // Round {r}")
        for i in range(d - 1):
            m1 = 2 * i + 1
            m2 = 2 * i + 2
            print(f"  %s{r}_{i} = qec.measure_parity %mzms#{m1}, %mzms#{m2} {{noise = {noise}}} : (!qec.mzm<{m1}, 0>, !qec.mzm<{m2}, 0>) -> !qec.syndrome")

        if r > 0:
            for i in range(d - 1):
                print(f"  qec.detector(%s{r}_{i}, %s{r-1}_{i}) : (!qec.syndrome, !qec.syndrome)")

    print(f"  %log = qec.logical_observable(%s{d-1}_0) : (!qec.syndrome) -> !qec.syndrome")
    print("}")

if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    noise = float(sys.argv[2]) if len(sys.argv) > 2 else 0.001
    gen_repetition(d, noise)
