option MINLP = BARON;
option optcr = 0;
option resLim = 1000;

set
    i
    t;

parameter
    r(i, t)
    r1(t)
    c
    l
    u;

$gdxIn %gdxincname%
$load i, t, r, r1, c, l, u
$gdxIn

variable z;
binary variable delta(i);
nonnegative variable x(i);

equation obj, ceiling, wholeness, lower_bound, upper_bound;

obj..
    z =e= sum(t, (sum(i, r(i, t) * x(i)) - r1(t)) * (sum(i, r(i, t) * x(i)) - r1(t)));
    
ceiling..
    sum(i, delta(i)) =e= c;

wholeness..
    sum(i, x(i)) =e= 1;

lower_bound(i)..
    x(i) =g= l*delta(i);

upper_bound(i)..
    x(i) =l= u*delta(i);

model index_tracking /obj, ceiling, wholeness, lower_bound, upper_bound/;
solve index_tracking using MINLP minimizing z;
display z.l, x.l, delta.l;
