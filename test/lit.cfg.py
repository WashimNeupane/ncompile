import os
import lit.formats

from lit.llvm import llvm_config

config.name = 'NCOMPILE'
config.test_format = lit.formats.ShTest(not llvm_config.use_lit_shell)
config.suffixes = ['.mlir']
config.test_source_root = os.path.dirname(__file__)

# Tweak the PATH to include the tools dir.
llvm_config.with_environment('PATH', config.ncompile_obj_root, append_path=True)

tool_dirs = [config.ncompile_obj_root + '/bin', '/home/washim/code/llvm-project/build/bin']
tools = ['qeccc-opt', 'FileCheck']

llvm_config.add_tool_substitutions(tools, tool_dirs)
