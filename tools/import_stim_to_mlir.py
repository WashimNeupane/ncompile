import stim
import sys

def import_stim(d, p_noise):
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=d,
        rounds=d,
        after_clifford_depolarization=p_noise
    )

    coords = circuit.get_final_qubit_coordinates()

    print("module {")

    # Define MZMs for all qubits in the circuit
    # Use a mapping to handle non-contiguous Stim qubit IDs
    qubit_ids = sorted(coords.keys())
    mzm_types = []
    stim_to_mlir_id = {}

    for i, q in enumerate(qubit_ids):
        c = coords[q]
        mzm_types.append(f"!qec.mzm<{int(c[0])}, {int(c[1])}>")
        stim_to_mlir_id[q] = i

    print(f"  %mzms:{len(qubit_ids)} = qec.mzm_init -> ({', '.join(mzm_types)})")

    ancilla_targets = {}
    measurement_to_syndrome = {}
    measurement_idx = 0
    p_str = f"{p_noise:.10f}"

    for instruction in circuit:
        if instruction.name == "CX":
            targets = instruction.targets_copy()
            for i in range(0, len(targets), 2):
                c = targets[i].value
                t = targets[i+1].value
                if t not in ancilla_targets: ancilla_targets[t] = []
                ancilla_targets[t].append(c)

        elif instruction.name == "MR" or instruction.name == "M":
            targets = instruction.targets_copy()
            for t in targets:
                q = t.value
                if q in ancilla_targets and ancilla_targets[q]:
                    data_qubits = ancilla_targets[q]
                    args = ", ".join([f"%mzms#{stim_to_mlir_id[dq]}" for dq in data_qubits])
                    m_coords = [coords[dq] for dq in data_qubits]
                    types = ", ".join([f"!qec.mzm<{int(c[0])}, {int(c[1])}>" for c in m_coords])

                    s_name = f"%s{measurement_idx}"
                    print(f"  {s_name} = qec.measure_parity {args} {{noise = {p_str}}} : ({types}) -> !qec.syndrome")
                    measurement_to_syndrome[measurement_idx] = s_name
                    ancilla_targets[q] = []
                else:
                    # Data measurement
                    mlir_id = stim_to_mlir_id[q]
                    c = coords[q]
                    print(f"  %m{measurement_idx} = qec.measure_parity %mzms#{mlir_id} {{noise = {p_str}}} : (!qec.mzm<{int(c[0])}, {int(c[1])}>) -> !qec.syndrome")
                    measurement_to_syndrome[measurement_idx] = f"%m{measurement_idx}"

                measurement_idx += 1

        elif instruction.name == "DETECTOR":
            targets = instruction.targets_copy()
            indices = []
            for t in targets:
                idx = measurement_idx + t.value
                if idx in measurement_to_syndrome:
                    indices.append(measurement_to_syndrome[idx])
            if indices:
                args = ", ".join(indices)
                types = ", ".join(["!qec.syndrome"] * len(indices))
                print(f"  qec.detector({args}) : ({types})")

        elif instruction.name == "OBSERVABLE_INCLUDE":
            targets = instruction.targets_copy()
            indices = []
            for t in targets:
                idx = measurement_idx + t.value
                if idx in measurement_to_syndrome:
                    indices.append(measurement_to_syndrome[idx])
            if indices:
                args = ", ".join(indices)
                types = ", ".join(["!qec.syndrome"] * len(indices))
                print(f"  %log = qec.logical_observable({args}) : ({types}) -> !qec.syndrome")

    print("}")

if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    p = float(sys.argv[2]) if len(sys.argv) > 2 else 0.001
    import_stim(d, p)
