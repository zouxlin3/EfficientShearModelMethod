wipe;
set dataDir F:/data_RSRP/SteelFrame3/ShearModelModal;
model BasicBuilder -ndm 2 -ndf 3;
set story 3;
node 0 0 0;
fix 0 1 1 1;
set mass {477.84999999999997 477.84999999999997 517.0}
set s1p {6469519.361370232 6463540.241492475 6498816.255058828}
set e1p {23.459622634944743 23.060341292049802 23.067482258004258}
set s2p {8496071.0 8559127.0 8622174.0}
set e2p {320.001 320.001 320.001}
set s3p {7335694.2147897445 7474668.111251325 7416233.468398053}
set e3p {320.32100099999997 320.64100199999996 320.32100099999997}
set s1n {-6315286.352458256 -6344380.003703944 -6351891.548548212}
set e1n {-22.793009803026603 -23.131021059415012 -22.197968740414264}
set s2n {-8496069.0 -8559112.0 -8622185.0}
set e2n {-319.999 -319.999 -319.999}
set s3n {-66358.8627811788 -4038867.43590942 -4763068.696078582}
set e3n {-320.31899899999996 -320.638998 -320.38756028733934}
set pinchX {0.001227946375328769 0.0010067647428158694 0.001}
set pinchY {0.5286775111144036 0.5139916479836468 0.5098480600766392}
set damage1 {0.001 0.001 0.0010071961550027746}
set damage2 {0.001 0.0014424756990491052 0.001012766527771887}
set beta {0.0021391550886330573 0.0010222969986318292 0.013749595778235634}
set height {3962.4 7924.8 11887.2}
for {set i 0} {$i < $story} {incr i} {
node [expr $i + 1] 0 [lindex $height $i];
mass [expr $i + 1] [lindex $mass $i] 0 0;
fix [expr $i + 1] 0 1 1;
uniaxialMaterial Hysteretic [expr $i + 1] [lindex $s1p $i] [lindex $e1p $i] [lindex $s2p $i] [lindex $e2p $i] [lindex $s3p $i] [lindex $e3p $i] \
[lindex $s1n $i] [lindex $e1n $i] [lindex $s2n $i] [lindex $e2n $i] [lindex $s3n $i] [lindex $e3n $i] \
[lindex $pinchX $i] [lindex $pinchY $i] [lindex $damage1 $i] [lindex $damage2 $i] [lindex $beta $i];
element twoNodeLink [expr $i + 1] $i [expr $i + 1] -mat [expr $i + 1] [expr $i + 1] [expr $i + 1] -dir 1 2 3;
};

file mkdir $dataDir;
source Units.tcl;
set lambda [eigen -fullGenLapack 3];
set lambda1 [lindex $lambda 0];
set lambda2 [lindex $lambda 1];
set lambda3 [lindex $lambda 2]; 
set omega1 [expr pow($lambda1, 0.5)];
set omega2 [expr pow($lambda2, 0.5)];
set omega3 [expr pow($lambda3, 0.5)];
set T1 [expr 2 * $PI / $omega1];
set T2 [expr 2 * $PI / $omega2];
set T3 [expr 2 * $PI / $omega3];
set f1 [expr 1 / $T1];
set f2 [expr 1 / $T2];
set f3 [expr 1 / $T3];
puts "T1= $T1 s";
puts "T2= $T2 s";
puts "T3= $T3 s";
puts "f1= [expr 1 / $T1] Hz";
puts "f2= [expr 1 / $T2] Hz";
puts "f3= [expr 1 / $T3] Hz";
puts "w1= [expr $omega1] rad/s";
puts "w2= [expr $omega2] rad/s";
puts "w3= [expr $omega3] rad/s";

set fileT [open $dataDir/ParamsModal.txt w];
puts $fileT "T (s): $T1, $T2, $T3";
puts $fileT "f (Hz): $f1, $f2, $f3";
puts $fileT "w (rad/s): $omega1, $omega2, $omega3";
close $fileT;
recorder Node -file $dataDir/Eigen1.txt -node 1 2 -dof 1 "eigen 1";
recorder Node -file $dataDir/Eigen2.txt -node 1 2 -dof 1 "eigen 2";
recorder Node -file $dataDir/Eigen3.txt -node 1 2 -dof 1 "eigen 3";
record;
puts "Successfully Finished!";
