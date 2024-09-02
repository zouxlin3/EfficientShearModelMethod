wipe;
set dataDir F:/data_RSRP/SteelFrame/Modal;
file mkdir $dataDir;
set TargetFloor 0;
source Units.tcl;
source BuildModel.tcl;
source Gravity.tcl;

set lambda [eigen -fullGenLapack 5];
set lambda1 [lindex $lambda 0];
set lambda2 [lindex $lambda 1];
set lambda3 [lindex $lambda 2];
set lambda4 [lindex $lambda 3];
set lambda5 [lindex $lambda 4];
set omega1 [expr pow($lambda1, 0.5)];
set omega2 [expr pow($lambda2, 0.5)];
set omega3 [expr pow($lambda3, 0.5)];
set omega4 [expr pow($lambda4, 0.5)];
set omega5 [expr pow($lambda5, 0.5)];
set T1 [expr 2 * $PI / $omega1];
set T2 [expr 2 * $PI / $omega2];
set T3 [expr 2 * $PI / $omega3];
set T4 [expr 2 * $PI / $omega4];
set T5 [expr 2 * $PI / $omega5];
set f1 [expr 1 / $T1];
set f2 [expr 1 / $T2];
set f3 [expr 1 / $T3];
set f4 [expr 1 / $T4];
set f5 [expr 1 / $T5];
puts "T1= $T1 s";
puts "T2= $T2 s";
puts "T3= $T3 s";
puts "T4= $T4 s";
puts "T5= $T5 s";
puts "f1= [expr 1 / $T1] Hz";
puts "f2= [expr 1 / $T2] Hz";
puts "f3= [expr 1 / $T3] Hz";
puts "f4= [expr 1 / $T4] Hz";
puts "f5= [expr 1 / $T5] Hz";
puts "w1= [expr $omega1] rad/s";
puts "w2= [expr $omega2] rad/s";
puts "w3= [expr $omega3] rad/s";
puts "w4= [expr $omega4] rad/s";
puts "w5= [expr $omega5] rad/s";

set fileT [open $dataDir/ParamsModal.txt w];
puts $fileT "T (s): $T1, $T2, $T3, $T4, $T5";
puts $fileT "f (Hz): $f1, $f2, $f3, $f4, $f5";
puts $fileT "w (rad/s): $omega1, $omega2, $omega3, $omega4, $omega5";
close $fileT;
recorder Node -file $dataDir/Eigen1.txt -node 1 2 -dof 1 "eigen 1";
recorder Node -file $dataDir/Eigen2.txt -node 1 2 -dof 1 "eigen 2";
recorder Node -file $dataDir/Eigen3.txt -node 1 2 -dof 1 "eigen 3";
recorder Node -file $dataDir/Eigen3.txt -node 1 2 -dof 1 "eigen 4";
recorder Node -file $dataDir/Eigen3.txt -node 1 2 -dof 1 "eigen 5";
record;
puts "Successfully Finished!";
