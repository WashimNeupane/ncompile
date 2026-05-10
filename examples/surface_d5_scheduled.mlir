module {
  %0:25 = qec.mzm_init -> (!qec.mzm<1, 1>, !qec.mzm<3, 1>, !qec.mzm<5, 1>, !qec.mzm<7, 1>, !qec.mzm<9, 1>, !qec.mzm<1, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 3>, !qec.mzm<7, 3>, !qec.mzm<9, 3>, !qec.mzm<1, 5>, !qec.mzm<3, 5>, !qec.mzm<5, 5>, !qec.mzm<7, 5>, !qec.mzm<9, 5>, !qec.mzm<1, 7>, !qec.mzm<3, 7>, !qec.mzm<5, 7>, !qec.mzm<7, 7>, !qec.mzm<9, 7>, !qec.mzm<1, 9>, !qec.mzm<3, 9>, !qec.mzm<5, 9>, !qec.mzm<7, 9>, !qec.mzm<9, 9>)
  %1 = qec.measure_parity %0#1, %0#0 {time_slice = 0 : i32} : (!qec.mzm<3, 1>, !qec.mzm<1, 1>) -> !qec.syndrome
  %2 = qec.measure_parity %0#3, %0#2 {time_slice = 0 : i32} : (!qec.mzm<7, 1>, !qec.mzm<5, 1>) -> !qec.syndrome
  %3 = qec.measure_parity %0#6, %0#1, %0#5, %0#0 {time_slice = 1 : i32} : (!qec.mzm<3, 3>, !qec.mzm<3, 1>, !qec.mzm<1, 3>, !qec.mzm<1, 1>) -> !qec.syndrome
  %4 = qec.measure_parity %0#7, %0#6, %0#2, %0#1 {time_slice = 2 : i32} : (!qec.mzm<5, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 1>, !qec.mzm<3, 1>) -> !qec.syndrome
  %5 = qec.measure_parity %0#8, %0#3, %0#7, %0#2 {time_slice = 3 : i32} : (!qec.mzm<7, 3>, !qec.mzm<7, 1>, !qec.mzm<5, 3>, !qec.mzm<5, 1>) -> !qec.syndrome
  %6 = qec.measure_parity %0#9, %0#8, %0#4, %0#3 {time_slice = 4 : i32} : (!qec.mzm<9, 3>, !qec.mzm<7, 3>, !qec.mzm<9, 1>, !qec.mzm<7, 1>) -> !qec.syndrome
  %7 = qec.measure_parity %0#9, %0#4 {time_slice = 5 : i32} : (!qec.mzm<9, 3>, !qec.mzm<9, 1>) -> !qec.syndrome
  %8 = qec.measure_parity %0#10, %0#5 {time_slice = 2 : i32} : (!qec.mzm<1, 5>, !qec.mzm<1, 3>) -> !qec.syndrome
  %9 = qec.measure_parity %0#11, %0#10, %0#6, %0#5 {time_slice = 3 : i32} : (!qec.mzm<3, 5>, !qec.mzm<1, 5>, !qec.mzm<3, 3>, !qec.mzm<1, 3>) -> !qec.syndrome
  %10 = qec.measure_parity %0#12, %0#7, %0#11, %0#6 {time_slice = 4 : i32} : (!qec.mzm<5, 5>, !qec.mzm<5, 3>, !qec.mzm<3, 5>, !qec.mzm<3, 3>) -> !qec.syndrome
  %11 = qec.measure_parity %0#13, %0#12, %0#8, %0#7 {time_slice = 5 : i32} : (!qec.mzm<7, 5>, !qec.mzm<5, 5>, !qec.mzm<7, 3>, !qec.mzm<5, 3>) -> !qec.syndrome
  %12 = qec.measure_parity %0#14, %0#9, %0#13, %0#8 {time_slice = 6 : i32} : (!qec.mzm<9, 5>, !qec.mzm<9, 3>, !qec.mzm<7, 5>, !qec.mzm<7, 3>) -> !qec.syndrome
  %13 = qec.measure_parity %0#16, %0#11, %0#15, %0#10 {time_slice = 5 : i32} : (!qec.mzm<3, 7>, !qec.mzm<3, 5>, !qec.mzm<1, 7>, !qec.mzm<1, 5>) -> !qec.syndrome
  %14 = qec.measure_parity %0#17, %0#16, %0#12, %0#11 {time_slice = 6 : i32} : (!qec.mzm<5, 7>, !qec.mzm<3, 7>, !qec.mzm<5, 5>, !qec.mzm<3, 5>) -> !qec.syndrome
  %15 = qec.measure_parity %0#18, %0#13, %0#17, %0#12 {time_slice = 7 : i32} : (!qec.mzm<7, 7>, !qec.mzm<7, 5>, !qec.mzm<5, 7>, !qec.mzm<5, 5>) -> !qec.syndrome
  %16 = qec.measure_parity %0#19, %0#18, %0#14, %0#13 {time_slice = 8 : i32} : (!qec.mzm<9, 7>, !qec.mzm<7, 7>, !qec.mzm<9, 5>, !qec.mzm<7, 5>) -> !qec.syndrome
  %17 = qec.measure_parity %0#19, %0#14 {time_slice = 9 : i32} : (!qec.mzm<9, 7>, !qec.mzm<9, 5>) -> !qec.syndrome
  %18 = qec.measure_parity %0#20, %0#15 {time_slice = 6 : i32} : (!qec.mzm<1, 9>, !qec.mzm<1, 7>) -> !qec.syndrome
  %19 = qec.measure_parity %0#21, %0#20, %0#16, %0#15 {time_slice = 7 : i32} : (!qec.mzm<3, 9>, !qec.mzm<1, 9>, !qec.mzm<3, 7>, !qec.mzm<1, 7>) -> !qec.syndrome
  %20 = qec.measure_parity %0#22, %0#17, %0#21, %0#16 {time_slice = 8 : i32} : (!qec.mzm<5, 9>, !qec.mzm<5, 7>, !qec.mzm<3, 9>, !qec.mzm<3, 7>) -> !qec.syndrome
  %21 = qec.measure_parity %0#23, %0#22, %0#18, %0#17 {time_slice = 9 : i32} : (!qec.mzm<7, 9>, !qec.mzm<5, 9>, !qec.mzm<7, 7>, !qec.mzm<5, 7>) -> !qec.syndrome
  %22 = qec.measure_parity %0#24, %0#19, %0#23, %0#18 {time_slice = 10 : i32} : (!qec.mzm<9, 9>, !qec.mzm<9, 7>, !qec.mzm<7, 9>, !qec.mzm<7, 7>) -> !qec.syndrome
  %23 = qec.measure_parity %0#22, %0#21 {time_slice = 10 : i32} : (!qec.mzm<5, 9>, !qec.mzm<3, 9>) -> !qec.syndrome
  %24 = qec.measure_parity %0#24, %0#23 {time_slice = 11 : i32} : (!qec.mzm<9, 9>, !qec.mzm<7, 9>) -> !qec.syndrome
}
