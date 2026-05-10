import stim, sys

def import_stim(d, p_noise=0.0):
    """
    Generate MLIR representing ONE round of syndrome extraction.
    No noise, no detectors — just the check structure.
    The translator will reconstruct the full circuit.
    """
    # Use rounds=1 to get clean single-round structure
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=d,
        rounds=1,
        after_clifford_depolarization=0.0  # NO noise in MLIR
    ).flattened()

    coords = circuit.get_final_qubit_coordinates()

    # Identify ancillas: qubits that are reset-and-measured (MR)
    ancilla_qubits = set()
    for inst in circuit:
        if inst.name == "MR":
            for t in inst.targets_copy():
                ancilla_qubits.add(t.value)

    # Build check structure: ancilla → list of data qubits it measures
    ancilla_fanin = {q: [] for q in ancilla_qubits}
    for inst in circuit:
        if inst.name == "CX":
            targets = inst.targets_copy()
            for i in range(0, len(targets), 2):
                ctrl, tgt = targets[i].value, targets[i+1].value
                if ctrl in ancilla_qubits:
                    ancilla_fanin[ctrl].append(tgt)
                elif tgt in ancilla_qubits:
                    ancilla_fanin[tgt].append(ctrl)

    # Collect data qubits only (not ancillas) for MZM representation
    data_qubits = sorted(q for q in coords if q not in ancilla_qubits)
    stim_to_mlir = {q: i for i, q in enumerate(data_qubits)}
    mzm_types = [
        f"!qec.mzm<{int(coords[q][0])}, {int(coords[q][1])}>"
        for q in data_qubits
    ]

    print("module {")
    print(f"  %mzms:{len(data_qubits)} = qec.mzm_init -> ({', '.join(mzm_types)})")

    check_idx = 0
    # Emit one measure_parity per stabilizer check
    for ancilla in sorted(ancilla_fanin.keys()):
        dqs = ancilla_fanin[ancilla]
        if not dqs:
            continue
        # Deduplicate preserving order
        seen = []
        for dq in dqs:
            if dq not in seen and dq in stim_to_mlir:
                seen.append(dq)
        if not seen:
            continue
        args  = ", ".join(f"%mzms#{stim_to_mlir[dq]}" for dq in seen)
        types = ", ".join(
            f"!qec.mzm<{int(coords[dq][0])}, {int(coords[dq][1])}>"
            for dq in seen
        )
        print(f"  %c{check_idx} = qec.measure_parity {args} : ({types}) -> !qec.syndrome")
        check_idx += 1

    print("}")

if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    import_stim(d)
