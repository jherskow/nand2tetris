@256
D=A
@SP
M=D
@_ret_0
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
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@$Sys.init
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
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
@R14
M=D
@SP
A=M
A=A-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
@1
D=D+A
@SP
M=D
@R13
D=M
@1
D=D-A
@THAT
M=D
@R13
D=M
@2
D=D-A
@THIS
M=D
@R13
D=M
@3
D=D-A
@ARG
M=D
@R13
D=M
@4
D=D-A
@LCL
M=D
R14
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
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci$Main.fibonacci
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
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci$Main.fibonacci
0;JMP
(FibonacciElement_ret_2)
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
@R14
M=D
@SP
A=M
A=A-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
@1
D=D+A
@SP
M=D
@R13
D=M
@1
D=D-A
@THAT
M=D
@R13
D=M
@2
D=D-A
@THIS
M=D
@R13
D=M
@3
D=D-A
@ARG
M=D
@R13
D=M
@4
D=D-A
@LCL
M=D
R14
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
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init$Main.fibonacci
0;JMP
(FibonacciElement_ret_3)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
