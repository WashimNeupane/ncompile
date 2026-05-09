#include "mlir/Bindings/Python/NanobindAdaptors.h"
#include "ncompile-c/Dialect/QEC.h"
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

namespace nb = nanobind;

NB_MODULE(_ncompileDialectsQEC, m) {
  m.doc() = "ncompile QEC dialect Python extension";

  m.def(
      "register_dialect",
      [](MlirContext context) {
        MlirDialectHandle handle = mlirGetDialectHandle__qec__();
        mlirDialectHandleRegisterDialect(handle, context);
        mlirDialectHandleLoadDialect(handle, context);
      },
      nb::arg("context"),
      "Registers and loads the QEC dialect in the given context.");

  mlir::python::nanobind_adaptors::mlir_type_subclass(
      m, "Qubit", ncompileMlirTypeIsAQECQubit)
      .def_staticmethod(
          "get",
          [](MlirContext ctx, int64_t x, int64_t y) {
            return ncompileMlirQECQubitTypeGet(ctx, x, y);
          },
          nb::arg("ctx"), nb::arg("x"), nb::arg("y"));

  mlir::python::nanobind_adaptors::mlir_type_subclass(
      m, "Syndrome", ncompileMlirTypeIsAQECSyndrome)
      .def_staticmethod(
          "get",
          [](MlirContext ctx) { return ncompileMlirQECSyndromeTypeGet(ctx); },
          nb::arg("ctx"));

  mlir::python::nanobind_adaptors::mlir_type_subclass(
      m, "Pauli", ncompileMlirTypeIsAQECPauli)
      .def_staticmethod(
          "get",
          [](std::string pauli, MlirContext ctx) {
            MlirStringRef msr =
                mlirStringRefCreate(pauli.c_str(), pauli.length());
            return ncompileMlirQECPauliTypeGet(ctx, msr);
          },
          nb::arg("pauli"), nb::arg("ctx"));

  mlir::python::nanobind_adaptors::mlir_type_subclass(m, "MZM",
                                                      ncompileMlirTypeIsAQECMZM)
      .def_staticmethod(
          "get",
          [](MlirContext ctx, int64_t x, int64_t y) {
            return ncompileMlirQECMZMTypeGet(ctx, x, y);
          },
          nb::arg("ctx"), nb::arg("x"), nb::arg("y"));

  mlir::python::nanobind_adaptors::mlir_type_subclass(
      m, "Tetron", ncompileMlirTypeIsAQECTetron)
      .def_staticmethod(
          "get",
          [](MlirContext ctx) { return ncompileMlirQECTetronTypeGet(ctx); },
          nb::arg("ctx"));
}
