"""
Orchestration script for running end-to-end QEC simulations.
Compares baseline Stim circuits against scheduled circuits using the ncompile toolchain.
Performs a threshold sweep across distances (d=3, 5, 7) and physical error rates (p).
"""
import subprocess
import stim
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import os

def get_stim_depth(stim_path):
    with open(stim_path, "r") as f:
        return f.read().count("TICK")

def get_scheduled_depth(stim_path):
    depth_file = stim_path + ".depth"
    if os.path.exists(depth_file):
        with open(depth_file) as f:
            return int(f.read().strip())
    return get_stim_depth(stim_path)

def run_sim(args):
    d, p, use_compiler = args

    os.makedirs("research_artifacts", exist_ok=True)

    if use_compiler:
        mlir_path = f"research_artifacts/surface_d{d}_p{p}.mlir"
        with open(mlir_path, "w") as f:
            subprocess.run(
                ["python3", "tools/import_stim_to_mlir.py", str(d)],
                stdout=f, stderr=subprocess.DEVNULL
            )
        scheduled_mlir = f"research_artifacts/surface_d{d}_p{p}_scheduled.mlir"
        with open(scheduled_mlir, "w") as f:
            subprocess.run(
                ["./build/bin/qeccc-opt", "--qec-schedule", mlir_path],
                stdout=f, stderr=subprocess.DEVNULL
            )
        stim_path = f"research_artifacts/surface_d{d}_p{p}_scheduled.stim"
        subprocess.run([
            "python3", "tools/apply_schedule_to_stim.py",
            scheduled_mlir, str(d), str(p), stim_path
        ], stderr=subprocess.DEVNULL)
        depth = get_scheduled_depth(stim_path)

    else:
        circuit = stim.Circuit.generated(
            "surface_code:rotated_memory_z",
            distance=d,
            rounds=d,
            after_clifford_depolarization=p
        )
        stim_path = f"research_artifacts/surface_d{d}_p{p}_baseline.stim"
        with open(stim_path, "w") as f:
            f.write(str(circuit))
        depth = get_stim_depth(stim_path)

    circuit = stim.Circuit.from_file(stim_path)

    # Adaptive shots: target ~200 errors minimum, cap at 200K for speed
    expected_L = p ** ((d + 1) // 2)
    num_shots = int(min(200000, max(50000, 200 / (expected_L + 1e-15))))

    sampler = circuit.compile_detector_sampler()
    defects, obs = sampler.sample(shots=num_shots, separate_observables=True)

    import pymatching
    dem = circuit.detector_error_model(
        decompose_errors=True,
        ignore_decomposition_failures=True
    )
    matching = pymatching.Matching.from_detector_error_model(dem)
    predictions = matching.decode_batch(defects)

    errors = int(np.sum(predictions != obs))
    L = errors / num_shots

    label = "Scheduled" if use_compiler else "Baseline"
    print(f"  d={d} p={p:.3f} {label:10s} -> L={L:.2e} ({errors}/{num_shots} shots, depth={depth})")

    return d, p, use_compiler, L, depth


def main():
    distances  = [3, 5, 7]
    error_rates = [0.005, 0.007, 0.01, 0.02, 0.03, 0.05, 0.07]

    # Build all (d, p, use_compiler) tasks
    tasks = [
        (d, p, use_compiler)
        for d in distances
        for p in error_rates
        for use_compiler in [True, False]
    ]

    print(f"Running {len(tasks)} simulations across {min(8, len(tasks))} workers...\n")

    with Pool(processes=min(8, len(tasks))) as pool:
        raw_results = pool.map(run_sim, tasks)

    # Collect results
    results_comp  = {d: {} for d in distances}
    results_base  = {d: {} for d in distances}
    depths_comp   = {d: 0  for d in distances}
    depths_base   = {d: 0  for d in distances}

    for d, p, use_compiler, L, depth in raw_results:
        if use_compiler:
            results_comp[d][p] = L
            depths_comp[d]     = depth
        else:
            results_base[d][p] = L
            depths_base[d]     = depth

    # Convert to ordered lists matching error_rates
    comp_lists = {d: [results_comp[d][p] for p in error_rates] for d in distances}
    base_lists = {d: [results_base[d][p] for p in error_rates] for d in distances}

    # Print depth summary
    print("\n--- Circuit Depth Summary ---")
    for d in distances:
        reduction = depths_base[d] / depths_comp[d] if depths_comp[d] > 0 else float('inf')
        print(f"  d={d}: Baseline={depths_base[d]} ticks, Scheduled={depths_comp[d]} ticks ({reduction:.2f}x reduction)")

    # Print raw logical error rates
    print("\n--- Raw Logical Error Rates ---")
    for d in distances:
        print(f"\n  Distance {d}:")
        for i, p in enumerate(error_rates):
            sched = comp_lists[d][i]
            base  = base_lists[d][i]
            ratio = base / sched if sched > 0 else float('inf')
            print(f"    p={p:.3f}: Scheduled={sched:.2e}  Baseline={base:.2e}  Improvement={ratio:.2f}x")

    # Plot
    plt.figure(figsize=(12, 8))
    colors = ['blue', 'orange', 'green']

    for i, d in enumerate(distances):
        plt.plot(error_rates, comp_lists[d], 'o-',
                 color=colors[i], linewidth=2, label=f'Scheduled d={d}')
        plt.plot(error_rates, base_lists[d], '--',
                 color=colors[i], alpha=0.5, label=f'Baseline d={d}')

    plt.plot(error_rates, error_rates, 'k:', alpha=0.5, label='L=p')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Physical Error Rate (p)', fontsize=13)
    plt.ylabel('Logical Error Rate (L)', fontsize=13)
    plt.title('Surface Code Logical Error Rate: Scheduled vs. Baseline Circuit Depth', fontsize=13)
    plt.legend(fontsize=11)
    plt.grid(True, which="both", ls="-", alpha=0.4)
    plt.tight_layout()
    plt.savefig('research_artifacts/surface_threshold_final.png', dpi=150)
    print("\nPlot saved to research_artifacts/surface_threshold_final.png")


if __name__ == "__main__":
    main()
