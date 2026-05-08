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

//===----------------------------------------------------------------------===//
// QEC Op definitions.
//===----------------------------------------------------------------------===//

class QEC_Op<string mnemonic, list<Trait> traits = []> :
        Op<QEC_Dialect, mnemonic, traits>;

#endif // QEC_DIALECT_TD
