module {
  %mzms:9 = qec.mzm_init -> (!qec.mzm<1, 1>, !qec.mzm<3, 1>, !qec.mzm<5, 1>, !qec.mzm<1, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 3>, !qec.mzm<1, 5>, !qec.mzm<3, 5>, !qec.mzm<5, 5>)
  %c0 = qec.measure_parity %mzms#1, %mzms#0 : (!qec.mzm<3, 1>, !qec.mzm<1, 1>) -> !qec.syndrome
  %c1 = qec.measure_parity %mzms#4, %mzms#1, %mzms#3, %mzms#0 : (!qec.mzm<3, 3>, !qec.mzm<3, 1>, !qec.mzm<1, 3>, !qec.mzm<1, 1>) -> !qec.syndrome
  %c2 = qec.measure_parity %mzms#5, %mzms#4, %mzms#2, %mzms#1 : (!qec.mzm<5, 3>, !qec.mzm<3, 3>, !qec.mzm<5, 1>, !qec.mzm<3, 1>) -> !qec.syndrome
  %c3 = qec.measure_parity %mzms#5, %mzms#2 : (!qec.mzm<5, 3>, !qec.mzm<5, 1>) -> !qec.syndrome
  %c4 = qec.measure_parity %mzms#6, %mzms#3 : (!qec.mzm<1, 5>, !qec.mzm<1, 3>) -> !qec.syndrome
  %c5 = qec.measure_parity %mzms#7, %mzms#6, %mzms#4, %mzms#3 : (!qec.mzm<3, 5>, !qec.mzm<1, 5>, !qec.mzm<3, 3>, !qec.mzm<1, 3>) -> !qec.syndrome
  %c6 = qec.measure_parity %mzms#8, %mzms#5, %mzms#7, %mzms#4 : (!qec.mzm<5, 5>, !qec.mzm<5, 3>, !qec.mzm<3, 5>, !qec.mzm<3, 3>) -> !qec.syndrome
  %c7 = qec.measure_parity %mzms#8, %mzms#7 : (!qec.mzm<5, 5>, !qec.mzm<3, 5>) -> !qec.syndrome
}
