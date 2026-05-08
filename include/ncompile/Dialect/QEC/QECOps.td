#ifndef QEC_OPS_TD
#define QEC_OPS_TD

include "QECDialect.td"
include "mlir/IR/OpBase.td"
include "mlir/Interfaces/SideEffectInterfaces.td"

//===----------------------------------------------------------------------===//
// Utility operations
//===----------------------------------------------------------------------===//

def PauliStrOp : QEC_Op<"pauli_str"> {
    let summary = "Define a Pauli string constant";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, StrAttr:$value);
    let results = (outs QEC_PauliType:$pauli);
    let assemblyFormat = "$value attr-dict `:` type($pauli)";
    let hasVerifier = 1;
}

def PatchConfigOp : QEC_Op<"patch_config"> {
    let summary = "Define a QEC patch configuration";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, StrAttr:$code_type, I64Attr:$distance);
    let results = (outs QEC_PatchType:$result);
    let assemblyFormat = "$code_type `,` $distance attr-dict `:` type($result)";
    let extraClassDeclaration = [{
        static void testVisibility() {}
    }];
}

//===----------------------------------------------------------------------===//
// High-level FT operations
//===----------------------------------------------------------------------===//

def InitializeOp : QEC_Op<"initialize"> {
    let summary = "Initialize a qubit register for a given code";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, StrAttr:$code_type, I64Attr:$distance);
    let results = (outs Variadic<QEC_QubitType>:$qubits);
    let assemblyFormat = "$code_type `,` $distance attr-dict `->` type($qubits)";
    let hasVerifier = 1;
}

def MeasurePauliOp : QEC_Op<"measure_pauli"> {
    let summary = "Measure a Pauli product over a set of qubits";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, Variadic<QEC_QubitType>:$qubits, QEC_PauliType:$pauli);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "`(` $qubits `)` `,` $pauli attr-dict `:` `(` type($qubits) `)` `,` type($pauli) `->` type($syndrome)";
    let hasVerifier = 1;
}

def DetectorOp : QEC_Op<"detector"> {
    let summary = "Declare a detector for measurement consistency";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, Variadic<QEC_SyndromeType>:$targets);
    let assemblyFormat = "`(` $targets `)` attr-dict `:` `(` type($targets) `)`";
    let hasVerifier = 1;
}

def LogicalObservableOp : QEC_Op<"logical_observable"> {
    let summary = "Declare a logical observable";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, Variadic<QEC_SyndromeType>:$targets);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "`(` $targets `)` attr-dict `:` `(` type($targets) `)` `->` type($syndrome)";
    let hasVerifier = 1;
}

//===----------------------------------------------------------------------===//
// Low-level Physical operations
//===----------------------------------------------------------------------===//

def CXOp : QEC_Op<"cx"> {
    let summary = "Controlled-X (CNOT) gate";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_QubitType:$control, QEC_QubitType:$target);
    let assemblyFormat = "$control `,` $target attr-dict `:` type($control) `,` type($target)";
    let hasVerifier = 1;
}

def ResetOp : QEC_Op<"reset"> {
    let summary = "Reset qubit to |0>";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_QubitType:$qubit);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit)";
}

def MeasureOp : QEC_Op<"measure"> {
    let summary = "Measure qubit in Z basis";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_QubitType:$qubit);
    let results = (outs QEC_SyndromeType:$syndrome);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit) `->` type($syndrome)";
}

def IdleOp : QEC_Op<"idle"> {
    let summary = "Idle operation for noise modeling";
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata, QEC_QubitType:$qubit);
    let assemblyFormat = "$qubit attr-dict `:` type($qubit)";
}

#endif // QEC_OPS_TD
