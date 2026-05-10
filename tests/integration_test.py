import subprocess
import stim
import pymatching
import numpy as np
import os
import sys

GROUND_TRUTH = {3: 1.94e-02, 5: 2.57e-02, 7: 2.58e-02}
EXPECTED_CHECKS = {3: 8, 5: 24, 7: 48}
EXPECTED_DETECTORS = {3: 24, 5: 120, 7: 336}

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout

def test_distance(d, p=0.01, shots=200000):
    print(f"\n--- Testing d={d} ---")

    mlir_path   = f"/tmp/test_d{d}.mlir"
    sched_path  = f"/tmp/test_d{d}_sched.mlir"
    stim_path   = f"/tmp/test_d{d}.stim"

    # Step 1: Generate MLIR
    run_cmd(f"python3 tools/import_stim_to_mlir.py {d} > {mlir_path}")
    check_count = int(run_cmd(f"grep 'measure_parity' {mlir_path} | wc -l").strip())
    assert check_count == EXPECTED_CHECKS[d], \
        f"d={d}: expected {EXPECTED_CHECKS[d]} checks, got {check_count}"
    print(f"  ✓ Check count: {check_count}")

    # Step 2: Schedule
    run_cmd(f"./build/bin/qeccc-opt --qec-schedule {mlir_path} > {sched_path}")

    non_mp_ts = int(run_cmd(
        f"grep 'time_slice' {sched_path} | grep -v 'measure_parity' | wc -l"
    ).strip())
    assert non_mp_ts == 0, f"d={d}: time_slice found on non-measure_parity ops"

    depth = int(run_cmd(
        f"grep 'measure_parity' {sched_path} | "
        f"grep -oP 'time_slice = \\K\\d+' | sort -n | uniq | wc -l"
    ).strip())
    assert depth < 14, f"d={d}: scheduled depth {depth} >= baseline 14"
    print(f"  ✓ Scheduled depth: {depth} (baseline: 14)")

    # Step 3: Translate
    run_cmd(f"python3 tools/apply_schedule_to_stim.py {sched_path} {d} {p} {stim_path}")

    circuit = stim.Circuit.from_file(stim_path)
    assert circuit.num_detectors == EXPECTED_DETECTORS[d], \
        f"d={d}: expected {EXPECTED_DETECTORS[d]} detectors, got {circuit.num_detectors}"
    assert circuit.num_observables == 1, \
        f"d={d}: expected 1 observable, got {circuit.num_observables}"
    print(f"  ✓ Circuit structure: {circuit.num_detectors} detectors, 1 observable")

    # Step 4: Logical error rate
    sampler = circuit.compile_detector_sampler()
    defects, obs = sampler.sample(shots=shots, separate_observables=True)
    dem = circuit.detector_error_model(
        decompose_errors=True, ignore_decomposition_failures=True
    )
    matching = pymatching.Matching.from_detector_error_model(dem)
    preds = matching.decode_batch(defects)
    L = float(np.sum(preds != obs)) / shots

    gt = GROUND_TRUTH[d]
    tolerance = 5e-03
    assert abs(L - gt) < tolerance, \
        f"d={d}: L={L:.2e} differs from ground truth {gt:.2e} by more than {tolerance:.2e}"
    print(f"  ✓ Logical error rate: L={L:.2e} (ground truth: {gt:.2e})")

    # Step 5: Sidecar depth
    sidecar = stim_path + ".depth"
    assert os.path.exists(sidecar), f"d={d}: sidecar depth file missing at {sidecar}"
    sidecar_depth = int(open(sidecar).read().strip())
    assert sidecar_depth == depth, \
        f"d={d}: sidecar depth {sidecar_depth} != MLIR depth {depth}"
    print(f"  ✓ Sidecar depth: {sidecar_depth}")

def main():
    print("ncompile Integration Test Suite")
    print("=" * 40)
    for d in [3, 5, 7]:
        test_distance(d)
    print("\n" + "=" * 40)
    print("ALL TESTS PASSED ✓")

if __name__ == "__main__":
    main()
