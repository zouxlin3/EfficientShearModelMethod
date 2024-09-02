wipe;
source DynSettings.tcl;
model BasicBuilder -ndm 2 -ndf 3;
set story 3;
node 0 0 0;
fix 0 1 1 1;
set mass {477.84999999999997 477.84999999999997 517.0}
set s1p {6473896.595991301 6463540.241492475 6507420.865713439}
set e1p {22.71639691389673 23.060341292049802 23.410725403256162}
set s2p {8496071.0 8559127.0 8622174.0}
set e2p {320.001 320.001 320.001}
set s3p {7581951.258966088 7474668.111251325 7425671.845032347}
set e3p {320.64100199999996 320.64100199999996 320.43946788871096}
set s1n {-6313928.131501598 -6344380.003703944 -6338393.891012735}
set e1n {-23.60840151927184 -23.131021059415012 -22.849826956714605}
set s2n {-8496069.0 -8559112.0 -8622185.0}
set e2n {-319.999 -319.999 -319.999}
set s3n {-5857576.206748295 -4038867.43590942 -179720.1996451478}
set e3n {-320.638998 -320.638998 -320.4778874542728}
set pinchX {0.0011603911750155114 0.0010067647428158694 0.0010050994668426307}
set pinchY {0.5218875495284371 0.5139916479836468 0.5108887227400941}
set damage1 {0.0015305215763019298 0.001 0.0010067881687995065}
set damage2 {0.001002349836387373 0.0014424756990491052 0.001}
set beta {0.0010917049724864887 0.0010222969986318292 0.003223503139602034}
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
set xDamp 0.05;
set nEigenI 1;
set nEigenJ 2;
set lambdaN [eigen -fullGenLapack [expr $nEigenJ]];
set lambdaI [lindex $lambdaN [expr $nEigenI - 1]];
set lambdaJ [lindex $lambdaN [expr $nEigenJ - 1]];
set omegaI [expr pow($lambdaI, 0.5)];
set omegaJ [expr pow($lambdaJ, 0.5)];
set alphaM [expr $xDamp * (2 * $omegaI * $omegaJ) / ($omegaI + $omegaJ)];
set betaKcurr [expr 2. * $xDamp / ($omegaI + $omegaJ)];
rayleigh $alphaM $betaKcurr 0 0;
timeSeries Path 2 -dt $dt -filePath $path_GMR -factor $factor;
pattern UniformExcitation 2 1 -accel 2;
file mkdir $dataDir;
for {set i 0} {$i < $story} {incr i} {
recorder Node -file $dataDir/Dyn_[expr $i + 1]_disp.out -time -node [expr $i + 1] -dof 1 disp;
recorder Node -file $dataDir/Dyn_[expr $i + 1]_vel.out -time -node [expr $i + 1] -dof 1 vel;
recorder Node -file $dataDir/Dyn_[expr $i + 1]_accel.out -timeSeries 2 -time -node [expr $i + 1] -dof 1 accel;
};
constraints Transformation;
numberer Plain;
system BandGeneral;
integrator Newmark 0.5 0.25;
test NormDispIncr 1.0e-4 10;
algorithm Newton;
analyze $npts $dt;
puts "Successfully finished!"
# source SmartAnalyze.tcl;
# SmartAnalyzeTransient $dt $npts;
