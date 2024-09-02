set NT 1.;
set mm 1.;
set sec 1.;

set meter [expr 1000 * $mm];
set kg [expr $NT / ($meter / pow($sec, 2))];
set t [expr 1000 * $kg];
set MPa [expr 1 * $NT / pow($mm, 2)];
set GPa [expr 1000 * $MPa];
set pi 3.1416;
set gram [expr $kg / 1000];
set cm [expr 10 * $mm];
set G [expr 9.80655 * $meter / pow($sec, 2)];
set kN [expr 1000 * $NT];
set PI [expr 2 * asin(1.0)];
set mm2 [expr $mm * $mm];
set mm4 [expr $mm * $mm * $mm * $mm];
