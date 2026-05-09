module {
  %mzms:4 = qec.mzm_init -> (!qec.mzm<0,0>, !qec.mzm<0,1>, !qec.mzm<10,10>, !qec.mzm<10,11>)
  %1 = qec.measure_parity %mzms#0, %mzms#1 : (!qec.mzm<0,0>, !qec.mzm<0,1>) -> !qec.syndrome
  %2 = qec.measure_parity %mzms#2, %mzms#3 : (!qec.mzm<10,10>, !qec.mzm<10,11>) -> !qec.syndrome
}
