/**
 * @file QECOps.td
 * @brief TableGen definition for QEC Operations.
 * @ingroup qec_dialect
 */

#ifndef QEC_OPS_TD
#define QEC_OPS_TD

include "QECDialect.td"
include "mlir/IR/OpBase.td"
include "mlir/Interfaces/SideEffectInterfaces.td"

//===----------------------------------------------------------------------===//
// Utility operations
//===----------------------------------------------------------------------===//

def PauliStrOp : QEC_Op<"pauli_str", [Pure]> {
    let summary = "Create a Pauli string constant";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, StrAttr:$value);
    let results = (outs QEC_PauliType:$res);
    let assemblyFormat = "$value attr-dict `:` type($res)";
}

def PatchConfigOp : QEC_Op<"patch_config", [Pure]> {
    let summary = "Configure a QEC patch";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, StrAttr:$code_type, I64Attr:$distance);
    let results = (outs QEC_PatchType:$res);
    let assemblyFormat = "$code_type `,` $distance attr-dict `:` type($res)";
}

//===----------------------------------------------------------------------===//
// High-level QEC operations
//===----------------------------------------------------------------------===//

def MZMInitOp : QEC_Op<"mzm_init", [MemoryEffects<[MemWrite]>]> {
    let summary = "Initialize a grid of Majorana Zero Modes";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata);
    let results = (outs Variadic<QEC_MZMType>:$mzms);
    let assemblyFormat = "attr-dict `->` `(` type($mzms) `)`";
}

def MeasureParityOp : QEC_Op<"measure_parity", [MemoryEffects<[MemWrite]>]> {
    let summary = "Measure the joint parity of a set of MZMs";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata,
                         Variadic<QEC_MZMType>:$mzms,
                         OptionalAttr<I32Attr>:$time_slice,
                         OptionalAttr<ArrayAttr>:$braid_path,
                         OptionalAttr<F64Attr>:$noise);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "$mzms attr-dict `:` functional-type($mzms, results)";
    let hasVerifier = 1;
}

def InitializeOp : QEC_Op<"initialize", [MemoryEffects<[MemWrite]>]> {
    let summary = "Initialize a qubit register for a given code";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_CodeType:$code_type, I64Attr:$distance);
    let results = (outs Variadic<QEC_QubitType>:$qubits);
    let assemblyFormat = "$code_type `,` $distance attr-dict `->` type($qubits)";
    let hasVerifier = 1;
}

def MeasurePauliOp : QEC_Op<"measure_pauli", [MemoryEffects<[MemWrite]>]> {
    let summary = "Measure a Pauli product over a set of qubits";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata,
                         Variadic<QEC_QubitType>:$qubits,
                         QEC_PauliType:$pauli,
                         OptionalAttr<I32Attr>:$time_slice);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "`(` $qubits `)` `,` $pauli attr-dict `:` `(` type($qubits) `)` `,` type($pauli) `->` type($syndrome)";
    let hasVerifier = 1;
}

def DetectorOp : QEC_Op<"detector", [MemoryEffects<[MemWrite]>]> {
    let summary = "Declare a detector for measurement consistency";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, Variadic<QEC_SyndromeType>:$targets);
    let assemblyFormat = "`(` $targets `)` attr-dict `:` `(` type($targets) `)`";
    let hasVerifier = 1;
}

def LogicalObservableOp : QEC_Op<"logical_observable", [MemoryEffects<[MemWrite]>]> {
    let summary = "Declare a logical observable";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, Variadic<QEC_SyndromeType>:$targets);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "`(` $targets `)` attr-dict `:` `(` type($targets) `)` `->` type($syndrome)";
    let hasVerifier = 1;
}

//===----------------------------------------------------------------------===//
// Low-level QEC operations
//===----------------------------------------------------------------------===//

def CXOp : QEC_Op<"cx", [MemoryEffects<[MemWrite]>]> {
    let summary = "Controlled-X (CNOT) gate";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_AnyResourceType:$control, QEC_AnyResourceType:$target);
    let assemblyFormat = "$control `,` $target attr-dict `:` type($control) `,` type($target)";
    let hasVerifier = 1;
}

def ResetOp : QEC_Op<"reset", [MemoryEffects<[MemWrite]>]> {
    let summary = "Reset qubit to |0>";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_AnyResourceType:$qubit);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit)";
}

def MeasureOp : QEC_Op<"measure", [MemoryEffects<[MemWrite]>]> {
    let summary = "Measure qubit in Z basis";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_AnyResourceType:$qubit);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit) `->` type($syndrome)";
}

def HOp : QEC_Op<"h", [MemoryEffects<[MemWrite]>]> {
    let summary = "Hadamard gate";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_AnyResourceType:$qubit);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit)";
}

def IdleOp : QEC_Op<"idle", [MemoryEffects<[MemWrite]>]> {
    let summary = "Idle (explicit no-op)";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_AnyResourceType:$qubit);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit)";
}

#endif // QEC_OPS_TD
