wipe;
source DynSettings.tcl;
file mkdir $dataDir;
source Units.tcl;
source BuildModel.tcl;
source Gravity.tcl;
source SmartAnalyze.tcl;

# 阻尼
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

# 地震动
timeSeries Path 2 -dt $dt -filePath $path_GMR -factor $factor;
pattern UniformExcitation 2 1 -accel 2;

for {set i 1} {$i <= 9} {incr i} {
  recorder Node -file $dataDir/Dyn_${i}_disp.out -time -node [expr ($i + 1) * 10 + 1] -dof 1 disp;
  recorder Node -file $dataDir/Dyn_${i}_vel.out -time -node [expr ($i + 1) * 10 + 1] -dof 1 vel;
  recorder Node -file $dataDir/Dyn_${i}_accel.out -timeSeries 2 -time -node [expr ($i + 1) * 10 + 1] -dof 1 accel;
};

# 时程分析
constraints Transformation;
numberer Plain;
system BandGeneral;
integrator Newmark 0.5 0.25;
SmartAnalyzeTransient $dt $npts;
