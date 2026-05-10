module {
  %0:9 = qec.mzm_init -> (!qec.mzm<1, 1>, !qec.mzm<3, 1>, !qec.mzm<5, 1>, !qec.mzm<1, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 3>, !qec.mzm<1, 5>, !qec.mzm<3, 5>, !qec.mzm<5, 5>)
  %1 = qec.measure_parity %0#1, %0#0 {time_slice = 0 : i32} : (!qec.mzm<3, 1>, !qec.mzm<1, 1>) -> !qec.syndrome
  %2 = qec.measure_parity %0#4, %0#1, %0#3, %0#0 {time_slice = 1 : i32} : (!qec.mzm<3, 3>, !qec.mzm<3, 1>, !qec.mzm<1, 3>, !qec.mzm<1, 1>) -> !qec.syndrome
  %3 = qec.measure_parity %0#5, %0#4, %0#2, %0#1 {time_slice = 2 : i32} : (!qec.mzm<5, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 1>, !qec.mzm<3, 1>) -> !qec.syndrome
  %4 = qec.measure_parity %0#5, %0#2 {time_slice = 3 : i32} : (!qec.mzm<5, 3>, !qec.mzm<5, 1>) -> !qec.syndrome
  %5 = qec.measure_parity %0#6, %0#3 {time_slice = 2 : i32} : (!qec.mzm<1, 5>, !qec.mzm<1, 3>) -> !qec.syndrome
  %6 = qec.measure_parity %0#7, %0#6, %0#4, %0#3 {time_slice = 3 : i32} : (!qec.mzm<3, 5>, !qec.mzm<1, 5>, !qec.mzm<3, 3>, !qec.mzm<1, 3>) -> !qec.syndrome
  %7 = qec.measure_parity %0#8, %0#5, %0#7, %0#4 {time_slice = 4 : i32} : (!qec.mzm<5, 5>, !qec.mzm<5, 3>, !qec.mzm<3, 5>, !qec.mzm<3, 3>) -> !qec.syndrome
  %8 = qec.measure_parity %0#8, %0#7 {time_slice = 5 : i32} : (!qec.mzm<5, 5>, !qec.mzm<3, 5>) -> !qec.syndrome
}
