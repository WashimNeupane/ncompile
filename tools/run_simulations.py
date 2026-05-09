import stim
import pymatching
import numpy as np
import subprocess
import os

def simulate_circuit(circuit_path, shots=10000):
    circuit = stim.Circuit.from_file(circuit_path)
    sampler = circuit.compile_detector_sampler()
    def_samples, obs_samples = sampler.sample(shots=shots, separate_observables=True)

    dem = circuit.detector_error_model(
        decompose_errors=True,
        ignore_decomposition_failures=True
    )
    matching = pymatching.Matching.from_detector_error_model(dem)
    predictions = matching.decode_batch(def_samples)

    num_errors = np.sum(np.any(predictions != obs_samples, axis=1))
    return num_errors / shots

def run_study():
    p_values = [0.05, 0.1]
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/washim/code/llvm-project/build/tools/mlir/python_packages/mlir_core:/home/washim/code/ncompile/build/python/python_packages"

    # 1. Generate Topological Repetition Code
    print("Generating Topological Repetition Code...")
    subprocess.run("python3 tools/gen_tetron_repetition_code.py > tetron_repetition.mlir", shell=True, env=env)

    # 2. Compile Physical Schedule
    print("Compiling Physical Schedule...")
    subprocess.run("./build/bin/qeccc-opt --qec-schedule tetron_repetition.mlir -o tetron_phys.mlir", shell=True)

    results = []
    for p in p_values:
        print(f"Simulating p={p}...")
        subprocess.run(f"./build/bin/qeccc-translate --qec-to-stim -p {p} tetron_phys.mlir > circuit.stim", shell=True)
        L = simulate_circuit("circuit.stim")
        results.append(L)

    print("\nFinal Results (Logical Error Rate L):")
    for p, L in zip(p_values, results):
        print(f"p={p}: L={L}")

if __name__ == "__main__":
    run_study()
