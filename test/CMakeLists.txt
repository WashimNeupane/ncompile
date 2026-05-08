set(NCOMPILE_SOURCE_DIR ${PROJECT_SOURCE_DIR})
set(NCOMPILE_BINARY_DIR ${PROJECT_BINARY_DIR})

configure_lit_site_cfg(
  ${CMAKE_CURRENT_SOURCE_DIR}/lit.site.cfg.py.in
  ${CMAKE_CURRENT_BINARY_DIR}/lit.site.cfg.py
  MAIN_CONFIG
  ${CMAKE_CURRENT_SOURCE_DIR}/lit.cfg.py
)

add_lit_testsuite(check-ncompile "Running the ncompile regression tests"
  ${CMAKE_CURRENT_BINARY_DIR}
  DEPENDS ncompile-opt
)

set_target_properties(check-ncompile PROPERTIES FOLDER "Tests")
