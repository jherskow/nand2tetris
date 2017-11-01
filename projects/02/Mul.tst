load Mul.hdl,
output-file Mul.out,
compare-to Mul.cmp,
output-list a%D1.16.1 b%D1.16.1 out%D1.16.1;

set a %D0,
set b %D1,
eval,
output;

set a %D1,
set b %D0,
eval,
output;

set a %D13,
set b %D56,
eval,
output;

set a %D-1,
set b %D0,
eval,
output;

set a %D0,
set b %D-1,
eval,
output;

set a %D-10,
set b %D6,
eval,
output;

set a %D15,
set b %D-3,
eval,
output;

set a %D-17,
set b %D-25,
eval,
output;



