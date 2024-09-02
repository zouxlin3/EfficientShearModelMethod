wipe;
source SpoSettings.tcl;
file mkdir $dataDir;
source Units.tcl;
source BuildModel.tcl;
source Gravity.tcl;
source SmartAnalyze.tcl;

recorder Node -file $dataDir/SPO_${TargetFloor}_disp.out -node [expr ($TargetFloor + 1) * 10 + 1] -dof 1 disp;
recorder Node -file $dataDir/SPO_${TargetFloor}_force.out -node [expr $TargetFloor * 10 + 1] [expr $TargetFloor * 10 + 2] [expr $TargetFloor * 10 + 3] [expr $TargetFloor * 10 + 4] [expr $TargetFloor * 10 + 5] -dof 1 reaction;

# 加载制度
set h [expr 4000 * $mm];
set Dincr [expr 10 * $mm];
set Ncycles 1;
set protocol {"0.0"};
foreach iD $iDmax {
  for {set i 1} {$i <= $Ncycles} {incr i 1} {
    set Dmax [expr $iD * $h];
    set protocol [concat $protocol "$Dmax -$Dmax"];
  };
};
set protocol [concat $protocol "0.0"];

# 加载模式
pattern Plain 2 Linear {
  load [expr ($TargetFloor + 1) * 10 + 1] 1 0 0;
  load [expr ($TargetFloor + 1) * 10 + 2] 1 0 0;
  load [expr ($TargetFloor + 1) * 10 + 3] 1 0 0;
  load [expr ($TargetFloor + 1) * 10 + 4] 1 0 0;
  load [expr ($TargetFloor + 1) * 10 + 5] 1 0 0;
};

# Pushover
constraints Plain;
numberer Plain;
system BandGeneral;
SmartAnalyzeStatic $IDctrlNode $IDctrlDOF $Dincr $protocol;
