import subprocess
import stim
import pymatching
import numpy as np
import matplotlib.pyplot as plt
import os

def run_simulation(L=6, p=0.005, shots=10000, naive=False):
    # 1. Generate scheduled/naive Stim circuit
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/washim/code/llvm-project/build/tools/mlir/python_packages/mlir_core:/home/washim/code/ncompile/build/python/python_packages"

    mode_flag = "naive=true" if naive else ""
    cmd = (f"python3 tools/gen_repetition_code.py | "
           f"./build/bin/qeccc-opt --qec-schedule='{mode_flag}' | "
           f"./build/bin/qeccc-translate --qec-to-stim -p {p}")

    circuit_str = subprocess.check_output(cmd, shell=True, env=env, text=True)
    circuit = stim.Circuit(circuit_str)

    # 2. Sample detections and observables
    sampler = circuit.compile_detector_sampler()
    def_samples, obs_samples = sampler.sample(shots=shots, separate_observables=True)

    # 3. Decode with PyMatching
    matching = pymatching.Matching.from_stim_circuit(circuit)
    predictions = matching.decode_batch(def_samples)

    # 4. Calculate Logical Error Rate
    num_errors = np.sum(np.any(predictions != obs_samples, axis=1))
    return num_errors / shots

def run_study():
    p_values = [0.001, 0.002, 0.005, 0.01, 0.02]
    results_opt = []
    results_naive = []

    print(f"{'p':<8} | {'Optimized L':<12} | {'Naive L':<12}")
    print("-" * 35)

    for p in p_values:
        l_opt = run_simulation(L=6, p=p, shots=5000, naive=False)
        l_naive = run_simulation(L=6, p=p, shots=5000, naive=True)

        results_opt.append(l_opt)
        results_naive.append(l_naive)
        print(f"{p:<8.3f} | {l_opt:<12.4f} | {l_naive:<12.4f}")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(p_values, results_opt, marker='o', label='Optimized (8 cycles)')
    plt.loglog(p_values, results_naive, marker='x', linestyle='--', label='Naive (72 cycles)')
    plt.title('Logical Error Rate: Optimized vs Naive Schedule')
    plt.xlabel('Physical Error Rate (p)')
    plt.ylabel('Logical Error Rate (L)')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()

    plot_path = "benchmarks/threshold_comparison.png"
    plt.savefig(plot_path)
    print(f"\nThreshold comparison saved to: {plot_path}")

if __name__ == "__main__":
    run_study()
