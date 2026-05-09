set(LLVM_LINK_COMPONENTS
    Support
)

add_mlir_tool(qeccc-translate
    qeccc-translate.cpp
)

target_link_libraries(qeccc-translate PRIVATE
    MLIRQECDialect
    MLIRStimTarget
    MLIRIR
    MLIRSupport
    MLIRTranslateLib
    MLIRRegisterAllDialects
)

mlir_check_all_link_libraries(qeccc-translate)
