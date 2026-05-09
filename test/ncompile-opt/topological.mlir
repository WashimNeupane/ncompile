// RUN: qeccc-opt %s | /home/washim/code/llvm-project/build/bin/FileCheck %s

// CHECK-LABEL: func @test_topological
func.func @test_topological() {
  %m0, %m1, %m2, %m3 = qec.mzm_init -> (!qec.mzm<0,0>, !qec.mzm<0,1>, !qec.mzm<1,0>, !qec.mzm<5,5>)

  // Valid parity measurement (distance 1)
  // CHECK: qec.measure_parity %{{.*}}#0, %{{.*}}#1 : (!qec.mzm<0, 0>, !qec.mzm<0, 1>) -> !qec.syndrome
  %s1 = qec.measure_parity %m0, %m1 {} : (!qec.mzm<0,0>, !qec.mzm<0,1>) -> !qec.syndrome

  return
}
