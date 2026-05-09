import subprocess
import re
import os
import matplotlib.pyplot as plt

def run_scaling_benchmark():
    L_values = [6, 8, 10, 12]
    results = []

    print(f"{'L':<5} | {'Qubits':<8} | {'Checks':<8} | {'Cycles':<8}")
    print("-" * 35)

    for L in L_values:
        n_qubits = 2 * L * L
        n_checks = 2 * L * L

        # 1. Generate IR
        # Set PYTHONPATH so the generator can find the dialects
        env = os.environ.copy()
        env["PYTHONPATH"] = "/home/washim/code/llvm-project/build/tools/mlir/python_packages/mlir_core:/home/washim/code/ncompile/build/python/python_packages"

        gen_cmd = f"python3 tools/gen_gross_code.py {L}"
        ir_content = subprocess.check_output(gen_cmd, shell=True, env=env, text=True)

        # 2. Run Scheduler
        opt_cmd = "./build/bin/qeccc-opt --qec-schedule"
        scheduled_ir = subprocess.run(opt_cmd, input=ir_content, shell=True, capture_output=True, text=True).stdout

        # 3. Count Cycles
        time_slices = re.findall(r"time_slice = ([0-9]+) : i32", scheduled_ir)
        if time_slices:
            max_cycle = max(int(c) for c in time_slices) + 1
        else:
            max_cycle = 0

        results.append((L, n_qubits, max_cycle))
        print(f"{L:<5} | {n_qubits:<8} | {n_checks:<8} | {max_cycle:<8}")

    # 4. Plot Results
    ls = [r[0] for r in results]
    qubits = [r[1] for r in results]
    cycles = [r[2] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(qubits, cycles, marker='o', linestyle='-', color='b', label='Greedy First-Fit')
    plt.title('Scheduler Scaling: Bivariate Bicycle Codes')
    plt.xlabel('Number of Qubits (n)')
    plt.ylabel('Total Cycles (Circuit Depth)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    plot_path = "benchmarks/scaling_results.png"
    plt.savefig(plot_path)
    print(f"\nPlot saved to: {plot_path}")

if __name__ == "__main__":
    run_scaling_benchmark()
