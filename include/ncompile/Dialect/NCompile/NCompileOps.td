#ifndef NCOMPILE_OPS
#define NCOMPILE_OPS

include "NCompileDialect.td"
include "mlir/IR/OpBase.td"
include "mlir/Interfaces/SideEffectInterfaces.td"

// Use properties for attributes to be compatible with modern MLIR
class NCompile_BaseOp<string mnemonic, list<Trait> traits = []> :
    NCompile_Op<mnemonic, traits> {
}

def ConstantOp : NCompile_BaseOp<"constant", [Pure]> {
    let summary = "constant operation";
    let arguments = (ins I64Attr:$value);
    let results = (outs I64:$res);

    let assemblyFormat = "$value attr-dict `->` type($res)";
}

def AddOp : NCompile_BaseOp<"add", [Pure]> {
    let summary = "add operation";
    let arguments = (ins I64:$lhs, I64:$rhs);
    let results = (outs I64:$res);

    let assemblyFormat = "$lhs `,` $rhs attr-dict `->` type($res)";
}

#endif // NCOMPILE_OPS
