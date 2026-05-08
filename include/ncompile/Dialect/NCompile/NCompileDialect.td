#ifndef NCOMPILE_DIALECT
#define NCOMPILE_DIALECT

include "mlir/IR/OpBase.td"

//===----------------------------------------------------------------------===//
// NCompile Dialect definition.
//===----------------------------------------------------------------------===//

def NCompile_Dialect : Dialect {
    let name = "ncompile";
    let summary = "A boilerplate dialect for ncompile.";
    let description = [{
        This dialect is a boilerplate for the ncompile compiler.
    }];
    let cppNamespace = "::mlir::ncompile";
}

//===----------------------------------------------------------------------===//
// Base NCompile operation definition.
//===----------------------------------------------------------------------===//

class NCompile_Op<string mnemonic, list<Trait> traits = []> :
        Op<NCompile_Dialect, mnemonic, traits>;

#endif // NCOMPILE_DIALECT
