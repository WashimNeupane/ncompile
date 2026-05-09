import subprocess
import stim

d = 3
p = 0.01

# Get your scheduled circuit
subprocess.run(["python3", "tools/import_stim_to_mlir.py", str(d), str(p)],
               stdout=open("test_input.mlir", "w"))
subprocess.run(["./build/bin/qeccc-opt", "--qec-schedule", "test_input.mlir"],
               stdout=open("test_scheduled.mlir", "w"))
subprocess.run(["./build/bin/qeccc-translate", "--qec-to-stim", "-p", str(p), "test_scheduled.mlir"],
               stdout=open("test_scheduled.stim", "w"))

# Get Stim baseline
baseline = stim.Circuit.generated(
    "surface_code:rotated_memory_z",
    distance=d, rounds=d,
    after_clifford_depolarization=p
)

# Print both and compare
print("=== YOUR SCHEDULED CIRCUIT ===")
with open("test_scheduled.stim") as f:
    print(f.read()[:2000])  # first 2000 chars

print("=== STIM BASELINE ===")
print(str(baseline)[:2000])
