@256
D=A
@SP
M=D
@_ret_0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@5
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Sys.init
0;JMP
(_ret_0)
(Main.fibonacci)
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
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@NEG10
D;JLT
@POS10
D;JGE
(NEG10)
@SP
A=M-1
A=A-1
D=M
@POS20
D;JGT
@CONT0
0;JMP
(POS10)
@SP
A=M-1
A=A-1
D=M
@NEG20
D;JLT
@CONT0
0;JMP
(POS20)
@SP
A=M-1
A=A-1
M=0
@SP
M=M-1
@ENDLABEL0
0;JMP
(NEG20)
@SP
A=M-1
A=A-1
M=-1
@SP
M=M-1
@ENDLABEL0
0;JMP
(CONT0)
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@TRUE0
D;JGE
@SP
A=M-1
M=-1
@ENDLABEL0
0;JMP
(TRUE0)
@SP
A=M-1
M=0
(ENDLABEL0)
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
@Main.fibonacci$IF_FALSE
0;JMP
(Main.fibonacci$IF_TRUE)
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
A=M
D=A
@R13
M=D
@R13
A=M
D=A
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
A=M
D=A
@1
D=D+A
@SP
M=D
@R13
A=M
D=A
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
A=M
D=A
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
A=M
D=A
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
A=M
D=A
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Main.fibonacci$IF_FALSE)
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
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@FibonacciElement_ret_1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@6
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Main.fibonacci
0;JMP
(FibonacciElement_ret_1)
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
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@FibonacciElement_ret_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@6
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Main.fibonacci
0;JMP
(FibonacciElement_ret_2)
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
A=M
D=A
@R13
M=D
@R13
A=M
D=A
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
A=M
D=A
@1
D=D+A
@SP
M=D
@R13
A=M
D=A
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
A=M
D=A
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
A=M
D=A
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
A=M
D=A
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@FibonacciElement_ret_3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@6
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Main.fibonacci
0;JMP
(FibonacciElement_ret_3)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
