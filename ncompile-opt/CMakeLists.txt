set(LLVM_LINK_COMPONENTS
    Support
)

add_mlir_tool(qeccc-opt
    qeccc-opt.cpp
)

target_link_libraries(qeccc-opt PRIVATE
    MLIRQECDialect
    MLIRIR
    MLIRPass
    MLIRSupport
    MLIROptLib
    MLIRRegisterAllDialects
    MLIRRegisterAllPasses
)

mlir_check_all_link_libraries(qeccc-opt)
