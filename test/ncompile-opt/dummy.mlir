// RUN: ncompile-opt %s | FileCheck %s

// CHECK: module
module {
  func.func @test(%arg0: i64) -> i64 {
    // CHECK: ncompile.add
    %0 = "ncompile.add"(%arg0, %arg0) : (i64, i64) -> i64
    return %0 : i64
  }
}
