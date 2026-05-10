import stim
import sys

def stim_to_qasm(d):
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=d,
        rounds=1,
        after_clifford_depolarization=0.0
    ).flattened()

    num_qubits = circuit.num_qubits
    print("OPENQASM 2.0;")
    print('include "qelib1.inc";')
    print(f"qreg q[{num_qubits}];")

    for inst in circuit:
        if inst.name == "CX":
            targets = inst.targets_copy()
            for i in range(0, len(targets), 2):
                print(f"cx q[{targets[i].value}],q[{targets[i+1].value}];")
        elif inst.name == "H":
            for t in inst.targets_copy():
                print(f"h q[{t.value}];")
        # TopoLS might not like reset/measure
        # elif inst.name == "R":
        #     for t in inst.targets_copy():
        #         print(f"reset q[{t.value}];")

if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    stim_to_qasm(d)
