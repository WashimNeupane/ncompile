module {
  %mzms:25 = qec.mzm_init -> (!qec.mzm<1, 1>, !qec.mzm<3, 1>, !qec.mzm<5, 1>, !qec.mzm<7, 1>, !qec.mzm<9, 1>, !qec.mzm<1, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 3>, !qec.mzm<7, 3>, !qec.mzm<9, 3>, !qec.mzm<1, 5>, !qec.mzm<3, 5>, !qec.mzm<5, 5>, !qec.mzm<7, 5>, !qec.mzm<9, 5>, !qec.mzm<1, 7>, !qec.mzm<3, 7>, !qec.mzm<5, 7>, !qec.mzm<7, 7>, !qec.mzm<9, 7>, !qec.mzm<1, 9>, !qec.mzm<3, 9>, !qec.mzm<5, 9>, !qec.mzm<7, 9>, !qec.mzm<9, 9>)
  %c0 = qec.measure_parity %mzms#1, %mzms#0 : (!qec.mzm<3, 1>, !qec.mzm<1, 1>) -> !qec.syndrome
  %c1 = qec.measure_parity %mzms#3, %mzms#2 : (!qec.mzm<7, 1>, !qec.mzm<5, 1>) -> !qec.syndrome
  %c2 = qec.measure_parity %mzms#6, %mzms#1, %mzms#5, %mzms#0 : (!qec.mzm<3, 3>, !qec.mzm<3, 1>, !qec.mzm<1, 3>, !qec.mzm<1, 1>) -> !qec.syndrome
  %c3 = qec.measure_parity %mzms#7, %mzms#6, %mzms#2, %mzms#1 : (!qec.mzm<5, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 1>, !qec.mzm<3, 1>) -> !qec.syndrome
  %c4 = qec.measure_parity %mzms#8, %mzms#3, %mzms#7, %mzms#2 : (!qec.mzm<7, 3>, !qec.mzm<7, 1>, !qec.mzm<5, 3>, !qec.mzm<5, 1>) -> !qec.syndrome
  %c5 = qec.measure_parity %mzms#9, %mzms#8, %mzms#4, %mzms#3 : (!qec.mzm<9, 3>, !qec.mzm<7, 3>, !qec.mzm<9, 1>, !qec.mzm<7, 1>) -> !qec.syndrome
  %c6 = qec.measure_parity %mzms#9, %mzms#4 : (!qec.mzm<9, 3>, !qec.mzm<9, 1>) -> !qec.syndrome
  %c7 = qec.measure_parity %mzms#10, %mzms#5 : (!qec.mzm<1, 5>, !qec.mzm<1, 3>) -> !qec.syndrome
  %c8 = qec.measure_parity %mzms#11, %mzms#10, %mzms#6, %mzms#5 : (!qec.mzm<3, 5>, !qec.mzm<1, 5>, !qec.mzm<3, 3>, !qec.mzm<1, 3>) -> !qec.syndrome
  %c9 = qec.measure_parity %mzms#12, %mzms#7, %mzms#11, %mzms#6 : (!qec.mzm<5, 5>, !qec.mzm<5, 3>, !qec.mzm<3, 5>, !qec.mzm<3, 3>) -> !qec.syndrome
  %c10 = qec.measure_parity %mzms#13, %mzms#12, %mzms#8, %mzms#7 : (!qec.mzm<7, 5>, !qec.mzm<5, 5>, !qec.mzm<7, 3>, !qec.mzm<5, 3>) -> !qec.syndrome
  %c11 = qec.measure_parity %mzms#14, %mzms#9, %mzms#13, %mzms#8 : (!qec.mzm<9, 5>, !qec.mzm<9, 3>, !qec.mzm<7, 5>, !qec.mzm<7, 3>) -> !qec.syndrome
  %c12 = qec.measure_parity %mzms#16, %mzms#11, %mzms#15, %mzms#10 : (!qec.mzm<3, 7>, !qec.mzm<3, 5>, !qec.mzm<1, 7>, !qec.mzm<1, 5>) -> !qec.syndrome
  %c13 = qec.measure_parity %mzms#17, %mzms#16, %mzms#12, %mzms#11 : (!qec.mzm<5, 7>, !qec.mzm<3, 7>, !qec.mzm<5, 5>, !qec.mzm<3, 5>) -> !qec.syndrome
  %c14 = qec.measure_parity %mzms#18, %mzms#13, %mzms#17, %mzms#12 : (!qec.mzm<7, 7>, !qec.mzm<7, 5>, !qec.mzm<5, 7>, !qec.mzm<5, 5>) -> !qec.syndrome
  %c15 = qec.measure_parity %mzms#19, %mzms#18, %mzms#14, %mzms#13 : (!qec.mzm<9, 7>, !qec.mzm<7, 7>, !qec.mzm<9, 5>, !qec.mzm<7, 5>) -> !qec.syndrome
  %c16 = qec.measure_parity %mzms#19, %mzms#14 : (!qec.mzm<9, 7>, !qec.mzm<9, 5>) -> !qec.syndrome
  %c17 = qec.measure_parity %mzms#20, %mzms#15 : (!qec.mzm<1, 9>, !qec.mzm<1, 7>) -> !qec.syndrome
  %c18 = qec.measure_parity %mzms#21, %mzms#20, %mzms#16, %mzms#15 : (!qec.mzm<3, 9>, !qec.mzm<1, 9>, !qec.mzm<3, 7>, !qec.mzm<1, 7>) -> !qec.syndrome
  %c19 = qec.measure_parity %mzms#22, %mzms#17, %mzms#21, %mzms#16 : (!qec.mzm<5, 9>, !qec.mzm<5, 7>, !qec.mzm<3, 9>, !qec.mzm<3, 7>) -> !qec.syndrome
  %c20 = qec.measure_parity %mzms#23, %mzms#22, %mzms#18, %mzms#17 : (!qec.mzm<7, 9>, !qec.mzm<5, 9>, !qec.mzm<7, 7>, !qec.mzm<5, 7>) -> !qec.syndrome
  %c21 = qec.measure_parity %mzms#24, %mzms#19, %mzms#23, %mzms#18 : (!qec.mzm<9, 9>, !qec.mzm<9, 7>, !qec.mzm<7, 9>, !qec.mzm<7, 7>) -> !qec.syndrome
  %c22 = qec.measure_parity %mzms#22, %mzms#21 : (!qec.mzm<5, 9>, !qec.mzm<3, 9>) -> !qec.syndrome
  %c23 = qec.measure_parity %mzms#24, %mzms#23 : (!qec.mzm<9, 9>, !qec.mzm<7, 9>) -> !qec.syndrome
}
