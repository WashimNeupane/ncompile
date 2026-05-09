from ._qec_ops_gen import *
from .._mlir_libs._ncompileDialectsQEC import *
from .._mlir_libs._ncompileDialectsQEC import register_dialect as _register_dialect_impl
from mlir.ir import *

def register_dialect(context=None):
  if context is None:
    context = Context.current
  _register_dialect_impl(context)
