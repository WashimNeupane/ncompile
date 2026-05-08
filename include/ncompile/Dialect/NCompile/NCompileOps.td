#ifndef NCOMPILE_OPS
#define NCOMPILE_OPS

include "NCompileDialect.td"
include "mlir/Interfaces/SideEffectInterfaces.td"

def ConstantOp : NCompile_Op<"constant", [Pure]> {
    let summary = "constant operation";
    let arguments = (ins I64Attr:$value);
    let results = (outs I64:$res);
}

def AddOp : NCompile_Op<"add", [Pure]> {
    let summary = "add operation";
    let arguments = (ins I64:$lhs, I64:$rhs);
    let results = (outs I64:$res);
}

#endif // NCOMPILE_OPS
