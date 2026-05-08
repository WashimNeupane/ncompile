set(LLVM_LINK_COMPONENTS
    Support
)

add_mlir_tool(ncompile-opt
    ncompile-opt.cpp
)

target_link_libraries(ncompile-opt PRIVATE
    MLIRNCompileDialect
    MLIRIR
    MLIRPass
    MLIRSupport
    MLIROptLib
    MLIRRegisterAllDialects
    MLIRRegisterAllPasses
)

mlir_check_all_link_libraries(ncompile-opt)
