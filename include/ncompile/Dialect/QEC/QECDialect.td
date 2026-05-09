/**
 * @file QECDialect.td
 * @brief TableGen definition for the QEC Dialect.
 * @ingroup qec_dialect
 */

#ifndef QEC_DIALECT_TD
#define QEC_DIALECT_TD

include "mlir/IR/OpBase.td"
include "mlir/IR/AttrTypeBase.td"
include "mlir/IR/EnumAttr.td"

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
// QEC Attributes and Enums.
//===----------------------------------------------------------------------===//

def QEC_CodeType : I32EnumAttr<"CodeType", "Supported QEC code types", [
  I32EnumAttrCase<"Surface", 0>,
  I32EnumAttrCase<"BivariateBicycle", 1>,
  I32EnumAttrCase<"Tetron", 2>
]> {
  let genSpecializedAttr = 1;
  let cppNamespace = "::mlir::qec";
}

//===----------------------------------------------------------------------===//
// QEC Type definitions.
//===----------------------------------------------------------------------===//

class QEC_Type<string name, string typeMnemonic, list<Trait> traits = []>
    : TypeDef<QEC_Dialect, name, traits> {
    let mnemonic = typeMnemonic;
}

def QEC_QubitType : QEC_Type<"Qubit", "qubit"> {
    let summary = "A physical qubit with coordinates";
    let parameters = (ins "int64_t":$x, "int64_t":$y);
    let assemblyFormat = "`<` $x `,` $y `>`";
}

def QEC_SyndromeType : QEC_Type<"Syndrome", "syndrome"> {
    let summary = "A syndrome measurement result (classical bit)";
}

def QEC_PauliType : QEC_Type<"Pauli", "pauli"> {
    let summary = "A Pauli string type";
    let parameters = (ins "StringAttr":$pauliString);
    let assemblyFormat = "`<` $pauliString `>`";
    let genVerifyDecl = 1;
}

def QEC_PatchType : QEC_Type<"Patch", "patch"> {
    let summary = "A QEC patch configuration";
    let parameters = (ins "StringAttr":$codeType, "int64_t":$distance);
    let assemblyFormat = "`<` $codeType `,` $distance `>`";
    let genVerifyDecl = 1;
}

//===----------------------------------------------------------------------===//
// QEC Op definition.
//===----------------------------------------------------------------------===//

class QEC_Op<string mnemonic, list<Trait> traits = []> :
    Op<QEC_Dialect, mnemonic, traits>;

#endif // QEC_DIALECT_TD
