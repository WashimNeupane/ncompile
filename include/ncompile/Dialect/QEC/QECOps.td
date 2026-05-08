#ifndef QEC_OPS
#define QEC_OPS

include "QECDialect.td"
include "mlir/IR/OpBase.td"
include "mlir/Interfaces/SideEffectInterfaces.td"

class QEC_BaseOp<string mnemonic, list<Trait> traits = []> :
    QEC_Op<mnemonic, traits> {
}

def ConstantOp : QEC_BaseOp<"constant", [Pure]> {
    let summary = "constant operation";
    let arguments = (ins I64Attr:$value);
    let results = (outs I64:$res);

    let assemblyFormat = "$value attr-dict `->` type($res)";
}

def AddOp : QEC_BaseOp<"add", [Pure]> {
    let summary = "add operation";
    let arguments = (ins I64:$lhs, I64:$rhs);
    let results = (outs I64:$res);

    let assemblyFormat = "$lhs `,` $rhs attr-dict `->` type($res)";
}

#endif // QEC_OPS
