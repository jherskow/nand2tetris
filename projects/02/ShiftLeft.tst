load ShiftLeft.hdl,
output-file ShiftLeft.out,
compare-to ShiftLeft.cmp,
output-list in%D1.16.1 out%D1.16.1;

set in %B0000000000000000,
eval,
output;

set in %B0000000000011010,
eval,
output;

set in %B1101111111111111,
eval,
output;

set in %B1100101010101010,
eval,
output;

set in %D250,
eval,
output;

set in %D-365,
eval,
output;
