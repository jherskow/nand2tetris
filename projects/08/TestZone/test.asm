(func)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=A
@R13
M=D
@R13
D=A
@5
D=D-A
@R14
M=D
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@ARG
D=A
@-1
D=D-A
@SP
M=D
@R13
D=A
@1
D=D-A
@THAT
M=D
@R13
D=A
@2
D=D-A
@THIS
M=D
@R13
D=A
@3
D=D-A
@ARG
M=D
@R13
D=A
@4
D=D-A
@LCL
M=D
@R14
0;JMP
@return_address_0
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=A
@6
D=D-A
@ARG
M=D
@SP
D=A
@LCL
M=D
@func
0;JMP
(return_address_0)
