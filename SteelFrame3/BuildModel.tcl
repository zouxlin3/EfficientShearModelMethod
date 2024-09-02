model BasicBuilder -ndm 2 -ndf 3;

# 几何参数
set LCol  [expr 3962.4  *  $mm];    
set LBeam  [expr 9144  *  $mm];
set NStory 3;
set NBay 4;

# 结点
set X1 0.;
set X2 [expr $X1 + $LBeam];
set X3 [expr $X2 + $LBeam];
set X4 [expr $X3 + $LBeam];
set X5 [expr $X4 + $LBeam];
set Y1 0.;
set Y2 [expr $Y1 + $LCol];
set Y3 [expr $Y2 + $LCol];
set Y4 [expr $Y3 + $LCol];
set XNodeCoord "$X1 $X2 $X3 $X4 $X5";
set YNodeCoord "$Y1 $Y2 $Y3 $Y4";
for {set level 1} {$level <=[expr $NStory+1]} {incr level 1} {
     set YNodeCoordi [lindex $YNodeCoord [expr $level - 1]];
     for {set pier 1} {$pier <= [expr $NBay + 1]} {incr pier 1} {
          set nodeID [expr $level  *  10 + $pier];
          set XNodeCoordi [lindex $XNodeCoord [expr $pier - 1]];
          node $nodeID $XNodeCoordi $YNodeCoordi;
     };
};
# 控制结点
set IDctrlNode [expr ($TargetFloor + 1)  *  10 + 1];
set IDctrlDOF 1;

# 约束
fix 11 1 1 1;
fix 12 1 1 1;
fix 13 1 1 1;
fix 14 1 1 1;
fix 15 1 1 1;
rigidLink beam 21 22;
rigidLink beam 22 23;
rigidLink beam 23 24;
rigidLink beam 24 25;
rigidLink beam 31 32;
rigidLink beam 32 33;
rigidLink beam 33 34;
rigidLink beam 34 35;
rigidLink beam 41 42;
rigidLink beam 42 43;
rigidLink beam 43 44;
rigidLink beam 44 45;
set Yi "$Y2 $Y3 $Y4";
for {set i 1} {$i < $TargetFloor} {incr i} {
   fixY [lindex $Yi [expr $i - 1]] 1 1 1;
};

# 材料
set Myw33x118axis3 [expr 1.522e9 * $NT * $mm];
set Myw30x116axis3 [expr 1.3918e9 * $NT * $mm];
set Myw24x68axis3 [expr 6.4671e8 * $NT * $mm];
set Myw18x35axis3 [expr 2.4722e8 * $NT * $mm];
set Myw16x26axis3 [expr 1.6133e8 * $NT * $mm];
set Myw14x257axis3 [expr 2.4521e9 * $NT * $mm];
set Myw14x311axis3 [expr 2.9786e9 * $NT * $mm];
set Myw14x68axis3 [expr 5.9128e8 * $NT * $mm];
set Es [expr 200000 * $MPa];
set EAbeam 1.0e10;
set EAw14x257 [expr $Es * 48576 * $mm2];
set EAw14x311 [expr $Es * 58524 * $mm2];
set EAw14x68 [expr $Es * 12390 * $mm2];
set EIw33x118axis3 [expr $Es * 2.4381e9 * $mm4];
set EIw30x116axis3 [expr $Es * 2.0346e9 * $mm4];
set EIw24x68axis3 [expr $Es * 7.4813e8 * $mm4];
set EIw18x35axis3 [expr $Es * 2.1342e8 * $mm4];
set EIw16x26axis3 [expr $Es * 1.2349e8 * $mm4];
set EIw14x257axis3 [expr $Es * 1.409e9 * $mm4];
set EIw14x311axis3 [expr $Es * 1.7897e9 * $mm4];
set EIw14x68axis3 [expr $Es * 2.9156e8 * $mm4];
set b 0.01;
set Axialbeam 1;
set Axialw14x257 2;
set Axialw14x311 3;
set Axialw14x68 4;
set Flexw33x118axis3 5;
set Flexw30x116axis3 6;
set Flexw24x68axis3 7;
set Flexw18x35axis3 8;
set Flexw16x26axis3 9;
set Flexw14x257axis3 10;
set Flexw14x311axis3 11;
set Flexw14x68axis3 12;
set Secw33x118axis3 13;
set Secw30x116axis3 14;
set Secw24x68axis3 15;
set Secw18x35axis3 16;
set Secw16x26axis3 17;
set Secw14x257axis3 18;
set Secw14x311axis3 19;
set Secw14x68axis3 20;
uniaxialMaterial Elastic $Axialbeam $EAbeam;
uniaxialMaterial Elastic $Axialw14x257 $EAw14x257;
uniaxialMaterial Elastic $Axialw14x311 $EAw14x311;
uniaxialMaterial Elastic $Axialw14x68 $EAw14x68;
uniaxialMaterial Steel01 $Flexw33x118axis3 $Myw33x118axis3 $EIw33x118axis3 $b;
uniaxialMaterial Steel01 $Flexw30x116axis3 $Myw30x116axis3 $EIw30x116axis3 $b;	
uniaxialMaterial Steel01 $Flexw24x68axis3 $Myw24x68axis3 $EIw24x68axis3 $b;
uniaxialMaterial Steel01 $Flexw18x35axis3 $Myw18x35axis3 $EIw18x35axis3 $b;
uniaxialMaterial Steel01 $Flexw16x26axis3 $Myw16x26axis3 $EIw16x26axis3 $b;
uniaxialMaterial Steel01 $Flexw14x257axis3 $Myw14x257axis3 $EIw14x257axis3 $b;
uniaxialMaterial Steel01 $Flexw14x311axis3 $Myw14x311axis3 $EIw14x311axis3 $b;
uniaxialMaterial Steel01 $Flexw14x68axis3 $Myw14x68axis3 $EIw14x68axis3 $b;

# 截面
section Aggregator $Secw33x118axis3 $Axialbeam P $Flexw33x118axis3 Mz;
section Aggregator $Secw30x116axis3 $Axialbeam P $Flexw30x116axis3 Mz;
section Aggregator $Secw24x68axis3 $Axialbeam P $Flexw24x68axis3 Mz;
section Aggregator $Secw18x35axis3 $Axialbeam P $Flexw18x35axis3 Mz;
section Aggregator $Secw16x26axis3 $Axialbeam P $Flexw16x26axis3 Mz;
section Aggregator $Secw14x257axis3 $Axialw14x257 P $Flexw14x257axis3 Mz;
section Aggregator $Secw14x311axis3 $Axialw14x311 P $Flexw14x311axis3 Mz;
section Aggregator $Secw14x68axis3 $Axialw14x68 P $Flexw14x68axis3 Mz;

# 单元
set IDColTransf 1;
set IDBeamTransf 2;
geomTransf PDelta $IDColTransf;
geomTransf Linear $IDBeamTransf;
set np 5;
# A列柱单元
for {set level 1} {$level <= 3} {incr level 1} {
      set nodeIDi [expr $level * 10 + 1];
      set nodeIDj [expr ($level + 1) * 10 + 1];
      set ColID $nodeIDi$nodeIDj;
      element nonlinearBeamColumn $ColID $nodeIDi $nodeIDj $np $Secw14x257axis3 $IDColTransf;
};
# B,C,D列柱单元
for {set level 1} {$level <= 3} {incr level 1} {
      for {set pier 2} {$pier <= 4} {incr pier 1} {
           set nodeIDi [expr $level * 10 + $pier];
           set nodeIDj [expr ($level + 1) * 10 + $pier];
           set ColID $nodeIDi$nodeIDj;
           element nonlinearBeamColumn $ColID $nodeIDi $nodeIDj $np $Secw14x311axis3 $IDColTransf;
      };
};
# E列柱单元
for {set level 1} {$level <= 3} {incr level 1} {
      set nodeIDi [expr $level * 10 + 5];
      set nodeIDj [expr ($level + 1) * 10 + 5];
      set ColID $nodeIDi$nodeIDj;
      element nonlinearBeamColumn $ColID $nodeIDi $nodeIDj $np $Secw14x68axis3 $IDColTransf;
};
# AB,BC,CD跨梁单元
set BeamSec "$Secw33x118axis3 $Secw30x116axis3 $Secw24x68axis3";
for {set level 2} {$level <= [expr $NStory + 1]} {incr level 1} {
     set BeamSecTag [lindex $BeamSec [expr $level - 2]];
     for {set pier 1} {$pier <= 3} {incr pier 1} { 
          set nodeIDi [expr $level * 10 + $pier];
          set nodeIDj [expr $level * 10 + $pier + 1];
          set BeamID $nodeIDi$nodeIDj;
          element nonlinearBeamColumn $BeamID $nodeIDi $nodeIDj $np $BeamSecTag $IDBeamTransf;
     };
};
# DE跨梁单元
element nonlinearBeamColumn 2425 24 25 $np $Secw18x35axis3 $IDBeamTransf;
element nonlinearBeamColumn 3435 34 35 $np $Secw18x35axis3 $IDBeamTransf;
element nonlinearBeamColumn 4445 44 45 $np $Secw16x26axis3 $IDBeamTransf;

# 质量
set m12 [expr 937164.9974 * $NT / $G];
set m3 [expr 1013963.045 * $NT / $G];
set M "$m12 $m12 $m3";
for {set level 2} {$level <= [expr $NStory + 1]} {incr level 1} {                
     set m [lindex $M [expr $level - 2]];
     for {set pier 1} {$pier <= [expr $NBay + 1]} {incr pier 1} {
          set nodeID [expr $level * 10 + $pier];
          mass $nodeID $m 0.0 0.0;
     };
};
