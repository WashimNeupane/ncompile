import subprocess
import os
import stim
import numpy as np
import matplotlib.pyplot as plt

def get_stim_depth(stim_path):
    with open(stim_path, "r") as f:
        return f.read().count("TICK")

def run_sim(d, p, use_compiler=True):
    if use_compiler:
        mlir_path = f"research_artifacts/surface_d{d}.mlir"
        with open(mlir_path, "w") as f:
            subprocess.run(["python3", "tools/import_stim_to_mlir.py", str(d), str(p)], stdout=f)

        scheduled_mlir = f"research_artifacts/surface_d{d}_scheduled.mlir"
        with open(scheduled_mlir, "w") as f:
            subprocess.run(["./build/bin/qeccc-opt", "--qec-schedule", mlir_path], stdout=f)

        stim_path = f"research_artifacts/surface_d{d}_scheduled.stim"
        with open(stim_path, "w") as f:
            subprocess.run(["./build/bin/qeccc-translate", "--qec-to-stim", "-p", str(p), scheduled_mlir], stdout=f)

        depth = get_stim_depth(stim_path)
    else:
        circuit = stim.Circuit.generated(
            "surface_code:rotated_memory_z",
            distance=d,
            rounds=d,
            after_clifford_depolarization=p
        )
        stim_path = f"research_artifacts/surface_d{d}_baseline.stim"
        with open(stim_path, "w") as f:
            f.write(str(circuit))
        depth = get_stim_depth(stim_path)

    circuit = stim.Circuit.from_file(stim_path)

    # ADAPTIVE SHOTS: Need more shots at low p for higher d
    # Baseline threshold is ~0.01, Scheduled is ~0.05
    # We target at least 100-200 errors for stable statistics
    # shots = 100 / expected_L
    # expected_L ~ p^((d+1)/2)
    # But let's cap it at 2M for speed
    num_shots = int(min(2000000, max(100000, 100 / (p**((d+1)//2) + 1e-12))))

    sampler = circuit.compile_detector_sampler()
    defects, obs = sampler.sample(shots=num_shots, separate_observables=True)

    import pymatching
    dem = circuit.detector_error_model(decompose_errors=True, ignore_decomposition_failures=True)
    matching = pymatching.Matching.from_detector_error_model(dem)
    predictions = matching.decode_batch(defects)

    errors = np.sum(predictions != obs)
    return errors / num_shots, depth

def main():
    distances = [3, 5, 7]
    # Error rates spanning both thresholds
    error_rates = [0.005, 0.007, 0.01, 0.02, 0.03, 0.05, 0.07]

    results_comp = {d: [] for d in distances}
    results_base = {d: [] for d in distances}
    depths_comp = {d: 0 for d in distances}
    depths_base = {d: 0 for d in distances}

    for d in distances:
        for p in error_rates:
            print(f"Simulating d={d}, p={p} (Scheduled)...")
            L, depth = run_sim(d, p, use_compiler=True)
            results_comp[d].append(L)
            depths_comp[d] = depth

            print(f"Simulating d={d}, p={p} (Baseline)...")
            L_base, depth_base = run_sim(d, p, use_compiler=False)
            results_base[d].append(L_base)
            depths_base[d] = depth_base

    print("\n--- Final Research Results ---")
    for d in distances:
        print(f"Distance {d}: Baseline Depth = {depths_base[d]}, Scheduled Depth = {depths_comp[d]} (Tax: {depths_comp[d]/depths_base[d]:.2f}x)")

    # Plotting
    plt.figure(figsize=(12, 8))
    colors = ['blue', 'orange', 'green']
    for i, d in enumerate(distances):
        plt.plot(error_rates, results_comp[d], 'o-', color=colors[i], label=f'Scheduled d={d}')
        plt.plot(error_rates, results_base[d], '--', color=colors[i], alpha=0.5, label=f'Baseline d={d}')

    plt.plot(error_rates, error_rates, 'k:', alpha=0.5, label='L=p')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Physical Error Rate (p)')
    plt.ylabel('Logical Error Rate (L)')
    plt.title('Topological Threshold Shift: Braiding-Aware QEC')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.savefig('research_artifacts/surface_threshold_final.png')
    print("\nSweep complete. Plot saved to research_artifacts/surface_threshold_final.png")

if __name__ == "__main__":
    main()
