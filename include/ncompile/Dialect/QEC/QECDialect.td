#ifndef QEC_DIALECT_TD
#define QEC_DIALECT_TD

include "mlir/IR/OpBase.td"
include "mlir/IR/AttrTypeBase.td"

//===----------------------------------------------------------------------===//
// QEC Dialect definition.
//===----------------------------------------------------------------------===//

def QEC_Dialect : Dialect {
    let name = "qec";
    let summary = "A dialect for Quantum Error Correction.";
    let description = [{
        This dialect represents fault-tolerant quantum error correction
        primitives and circuits.
    }];
    let cppNamespace = "::mlir::qec";
    let useDefaultTypePrinterParser = 1;
}

//===----------------------------------------------------------------------===//
// QEC Type definitions.
//===----------------------------------------------------------------------===//

class QEC_Type<string name, string typeMnemonic, list<Trait> traits = []>
    : TypeDef<QEC_Dialect, name, traits> {
  let mnemonic = typeMnemonic;
}

def QEC_QubitType : QEC_Type<"Qubit", "qubit"> {
  let summary = "A physical qubit in a QEC patch";
}

def QEC_SyndromeType : QEC_Type<"Syndrome", "syndrome"> {
  let summary = "A syndrome measurement result";
}

// Represents a Pauli string (e.g., "XYZI") as a type
def QEC_PauliType : QEC_Type<"Pauli", "pauli"> {
  let summary = "A Pauli string type";
  let parameters = (ins StringRefParameter<"The Pauli string">:$pauli_string);
  let assemblyFormat = "`<` $pauli_string `>`";
  let genVerifyDecl = 1;
}

// Represents a QEC code configuration (e.g., surface, distance 3)
def QEC_PatchType : QEC_Type<"Patch", "patch"> {
  let summary = "A QEC patch configuration type";
  let parameters = (ins StringRefParameter<"The code type">:$code_type,
                        AttrOrTypeParameter<"int64_t", "The distance">:$distance);
  let assemblyFormat = "`<` $code_type `,` $distance `>`";
  let genVerifyDecl = 1;
}

//===----------------------------------------------------------------------===//
// QEC Op definitions.
//===----------------------------------------------------------------------===//

// Base class for all QEC operations.
// It automatically appends an optional 'metadata' DictionaryAttr to the arguments.
// This forces mlir-tblgen to generate the mandatory Properties API boilerplate.
class QEC_Op<string mnemonic, list<Trait> traits = []> :
        Op<QEC_Dialect, mnemonic, traits> {
    let arguments = (ins OptionalAttr<DictionaryAttr>:$metadata);
}

#endif // QEC_DIALECT_TD
