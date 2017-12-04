C_PUSH = "push"
C_POP = "pop"


class CodeWriter:
    arithmeticCommands = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}
    segments = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

    def __init__(self, outPutFileName):
        self.__file = open(outPutFileName, 'w')
        self.__label_num = 0  # counter of labels number

    def writeArithmetic(self, command):
        """
        write assembly code that is equivalent to the given arithmetic command
        """
        if command == "add":
            self.add_command()
        elif command == "sub":
            self.sub_command()
        elif command == "neg":
            self.neg_command()
        elif command == "eq":
            self.eq_command()
            self.__label_num += 1
        elif command == "gt":
            self.gt_command()
            self.__label_num += 1
        elif command == "lt":
            self.lt_command()
            self.__label_num += 1
        elif command == "and":
            self.and_command()
        elif command == "or":
            self.or_command()
        elif command == "not":
            self.not_command()

    def add_command(self):
        """
        write assembly code that is equivalent an add command
        """
        self.__file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n")

    def sub_command(self):
        """
        write assembly code that is equivalent to a sub command
        """
        self.__file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n")

    def neg_command(self):
        """
        write assembly code that is equivalent to a neg command
        """
        self.__file.write("D=0\n@SP\nA=M-1\nM=D-M\n")

    def eq_command(self):
        """

        write assembly code that is the translation of the eq comparision command
        """
        self.__file.write("@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\n@CONDITION" + str(self.__label_num) + "\n" +
                          "D;" + "JEQ" + "\n@SP\nA=M-1\nM=0\n@CONTINUE" + str(
            self.__label_num) + "\n0;JMP\n(CONDITION" +
                          str(self.__label_num) + ")\n@SP\nA=M-1\nM=-1\n(CONTINUE" + str(self.__label_num) + ")\n")

    def gt_command(self):
        """
               write assembly code that is equivalent to a gt comparision command
         """
        self.__file.write("@SP\nA=M-1\nD=M\n@NEG1" + str(self.__label_num) + "\nD;JLT\n@POS1" + str(self.__label_num) +
                          "\nD;JGE\n(NEG1" + str(self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@POS2" + str(
            self.__label_num) + "\nD;JGT\n@CONT"
                          + str(self.__label_num) + "\n0;JMP\n(POS1" + str(
            self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@NEG2" +
                          str(self.__label_num) + "\nD;JLT\n@CONT" + str(self.__label_num) + "\n0;JMP\n(POS2" + str(
            self.__label_num) + ")\n@SP"
                                "\nA=M-1\nA=A-1\nM=-1\n@SP\nM=M-1\n@ENDLABEL" + str(
            self.__label_num) + "\n0;JMP\n(NEG2" + str(self.__label_num) + ")\n@SP" +
                          "\nA=M-1\nA=A-1\nM=0\n@SP\nM=M-1\n@ENDLABEL" + str(
            self.__label_num) + "\n0;JMP\n(CONT" + str(self.__label_num) + ")\n"
                                                                           "@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@TRUE" + str(
            self.__label_num) + "\nD;JGT\n@SP\nA=M-1\nM=0\n@ENDLABEL" +
                          str(self.__label_num) + "\n0;JMP\n(TRUE" + str(
            self.__label_num) + ")\n@SP\nA=M-1\nM=-1\n(ENDLABEL" +
                          str(self.__label_num) + ")\n")

    def lt_command(self):
        """

               write assembly code that is equivalent to a lt comparision command
               """
        self.__file.write("@SP\nA=M-1\nD=M\n@NEG1" + str(self.__label_num) + "\nD;JLT\n@POS1" + str(self.__label_num) +
                          "\nD;JGE\n(NEG1" + str(self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@POS2" + str(
            self.__label_num) + "\nD;JGT\n@CONT"
                          + str(self.__label_num) + "\n0;JMP\n(POS1" + str(
            self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@NEG2" +
                          str(self.__label_num) + "\nD;JLT\n@CONT" + str(self.__label_num) + "\n0;JMP\n(POS2" + str(
            self.__label_num) + ")\n@SP"
                                "\nA=M-1\nA=A-1\nM=0\n@SP\nM=M-1\n@ENDLABEL" + str(
            self.__label_num) + "\n0;JMP\n(NEG2" + str(self.__label_num) + ")\n@SP" +
                          "\nA=M-1\nA=A-1\nM=-1\n@SP\nM=M-1\n@ENDLABEL" + str(
            self.__label_num) + "\n0;JMP\n(CONT" + str(self.__label_num) + ")\n"
                                                                           "@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@TRUE" + str(
            self.__label_num) + "\nD;JGE\n@SP\nA=M-1\nM=-1\n@ENDLABEL" +
                          str(self.__label_num) + "\n0;JMP\n(TRUE" + str(
            self.__label_num) + ")\n@SP\nA=M-1\nM=0\n(ENDLABEL" +
                          str(self.__label_num) + ")\n")

    def and_command(self):
        """
        write assembly code that is the translation of and command
        """
        self.__file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n")

    def not_command(self):
        """
        write assembly code that is equivalent to a not command
        """
        self.__file.write("@SP\nA=M-1\nM=!M\n")

    def or_command(self):
        """
        write assembly code that is equivalent to an or command
        """
        self.__file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n")

    def writePushPop(self, command, segment, index):
        """
        write assembly code that is equivalent to a given command, where command is either C_PUSH or C_POP
        """
        if command == "C_PUSH":
            self.push_command(segment, int(index))
        elif command == "C_POP":
            self.pop_command(segment, int(index))

    def push_command(self, segment, index):
        """
        write assembly code that is equivalent to a push command
        """
        if segment == "constant": self.push_constant_segment(index)
        if segment in CodeWriter.segments:
            self.push_lcl_arg_this_that_segments(CodeWriter.segments.get(segment), index)
        if segment == "temp" or segment == "pointer":
            self.push_pointer_temp_segments(segment, index)
        if segment == "static":
            self.push_static_segment(index)

    def push_constant_segment(self, index):
        """ write the assembly code that is the translation of  "push constant index" command"""
        self.__file.write("@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_static_segment(self, index):
        """ write the assembly code that is the translation of "push static index " command"""
        address = str(16 + int(index))
        self.__file.write("@" + address + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_lcl_arg_this_that_segments(self, segment, index):
        """
        write the assembly code that is translation of "push (local\argument\this\that) index" command
        """
        self.__file.write("@" + segment + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_pointer_temp_segments(self, segment, index):
        """
        write the assembly code that is translation of "push (pointer\temp) index" command
        """
        if segment == "temp":
            index += 5
            address = "R5"
            self.__file.write("@" + address + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == "pointer":
            if index == 0:
                address = "THIS"
                self.__file.write("@" + address + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

            if index == 1:
                address = "THAT"
                self.__file.write("@" + address + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def pop_command(self, segment, index):
        """
        write the assembly code that translation of pop command
        """
        if segment in CodeWriter.segments:
            self.pop_lcl_arg_this_that_segments(CodeWriter.segments.get(segment), index)
        elif segment == "temp" or segment == "pointer":
            self.pop_temp_pointer_segments(segment, int(index))
        elif segment == "static":
            self.pop_static_segment(index)

    def pop_lcl_arg_this_that_segments(self, segment, index):
        """
        write the assembly code that translation of "pop (local\argument\this\that) index" command
        """
        self.__file.write(
            "@" + segment + "\nD=M\n@" + str(index) + "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def pop_temp_pointer_segments(self, segment, index):
        """
        write the assembly code that translation of "pop (temp\pointer) index" command
        """
        if segment == "temp":
            index += 5
            address = "R5"
            self.__file.write(
                "@" + address + "\nD=M\n@" + str(index) + "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
        elif segment == "pointer":
            if index == 0:
                address = "THIS"
                self.__file.write(
                    "@" + address + "\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            if index == 1:
                address = "THAT"
                self.__file.write(
                    "@" + address + "\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def pop_static_segment(self, index):
        """
        write the assembly code that is the translation of "pop static index" command
        """
        address = str(16 + index)
        self.__file.write(
            "@" + address + "\nD=M\n@" + str(index) + "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def push_zero_k_times(self,k):
        # todo
        for i in range(k):
            self.push_constant_segment(0) #todo

    def write_label(self, label):
        """Writes assembly code that effects the label command."""
        # make label name (f$b) or whatever
        # write (label_name)
        #

    def write_goto(self, label):
        """Writes assembly code that effects the goto command."""
        # @ f$label_name
        # 0:JMP
        #

    def write_if(self, label):
        """Writes assembly code that effects the if-goto command."""
        # @SP
        # D=M
        # @ f$label LABEL
        # D:JNE
        #


    def write_call(self, function_name, num_args):
        """Writes assembly code that effects the call command."""

    def write_return(self):
        """Writes assembly code that effects the return command."""

    def write_function(self,function_name, num_locals):
        """Writes assembly code that effects the function command."""

    def write_init(self, label):
        """Writes bootstrap code"""



    def close(self):
        """
        close an output file
        """
        self.__file.close()