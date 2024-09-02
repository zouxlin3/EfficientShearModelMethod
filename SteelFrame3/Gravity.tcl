# 重力荷载
set G12 [expr 156194.1662 * $NT];
set G3 [expr 168993.8408 * $NT];
set W "$G12 $G12 $G3";
pattern Plain 1 Linear {
    for {set level 2} {$level <= [expr $NStory + 1]} {incr level 1} {            
        set G1 [lindex $W [expr $level - 2]];
        for {set pier 1} {$pier <= [expr $NBay + 1]} {incr pier 1} {
            set nodeID [expr $level * 10 + $pier];
            load $nodeID 0.0 -$G1 0.0;
        };
    };
};

# 重力分析
constraints Transformation;
numberer RCM;
system SparseGeneral;
test EnergyIncr 1.e-2 20;
algorithm Newton;
integrator LoadControl 0.1;
analysis Static;
analyze 10;
loadConst -time 0.0;
