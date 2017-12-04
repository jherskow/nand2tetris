C_PUSH = "push"
C_POP = "pop"


class CodeWriter:
    arithmeticCommands = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}
    segments = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

    def __init__(self, out_filepath):
        self.__file = open(out_filepath, 'w')
        self.__label_num = 0  # counter of labels number
        self.__return_num = 0  # counter of labels number
        self.__filename = out_filepath.split("/")[-1].strip(".asm")

    def write_arithmetic(self, command):
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
        self.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n")

    def sub_command(self):
        """
        write assembly code that is equivalent to a sub command
        """
        self.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n")

    def neg_command(self):
        """
        write assembly code that is equivalent to a neg command
        """
        self.write("D=0\n@SP\nA=M-1\nM=D-M\n")

    def eq_command(self):
        """

        write assembly code that is the translation of the eq comparision command
        """
        self.write("@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\n@CONDITION" + str(self.__label_num) + "\n" +
                   "D;" + "JEQ" + "\n@SP\nA=M-1\nM=0\n@CONTINUE" + str(
            self.__label_num) + "\n0;JMP\n(CONDITION" +
                   str(self.__label_num) + ")\n@SP\nA=M-1\nM=-1\n(CONTINUE" + str(self.__label_num) + ")\n")

    def gt_command(self):
        """
               write assembly code that is equivalent to a gt comparision command
         """
        self.write(
            "@SP\nA=M-1\nD=M\n@NEG1" + str(self.__label_num) + "\nD;JLT\n@POS1" + str(self.__label_num) +
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
        self.write(
            "@SP\nA=M-1\nD=M\n@NEG1" + str(self.__label_num) + "\nD;JLT\n@POS1" + str(self.__label_num) +
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
        self.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n")

    def not_command(self):
        """
        write assembly code that is equivalent to a not command
        """
        self.write("@SP\nA=M-1\nM=!M\n")

    def or_command(self):
        """
        write assembly code that is equivalent to an or command
        """
        self.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n")

    def write_push_pop(self, command, segment, index):
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
        if segment == "constant":
            self.push_constant_segment(index)
        if segment in CodeWriter.segments:
            self.push_lcl_arg_this_that_segments(CodeWriter.segments.get(segment), index)
        if segment == "temp" or segment == "pointer":
            self.push_pointer_temp_segments(segment, index)
        if segment == "static":
            self.push_static_segment(index)

    def push_constant_segment(self, index):
        """ write the assembly code that is the translation of  "push constant index" command"""
        self.write("@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_static_segment(self, index):
        """ write the assembly code that is the translation of "push static index " command"""
        address = str(16 + int(index))
        self.write("@" + address + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_lcl_arg_this_that_segments(self, segment, index):
        """
        write the assembly code that is translation of "push (local\argument\this\that) index" command
        """
        self.write("@" + segment + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_pointer_temp_segments(self, segment, index):
        """
        write the assembly code that is translation of "push (pointer\temp) index" command
        """
        if segment == "temp":
            index += 5
            address = "R5"
            self.write("@" + address + "\nD=M\n@" + str(index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == "pointer":
            if index == 0:
                address = "THIS"
                self.write("@" + address + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

            if index == 1:
                address = "THAT"
                self.write("@" + address + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

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
        self.write(
            "@" + segment + "\nD=M\n@" + str(
                index) + "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def pop_temp_pointer_segments(self, segment, index):
        """
        write the assembly code that translation of "pop (temp\pointer) index" command
        """
        if segment == "temp":
            index += 5
            address = "R5"
            self.write(
                "@" + address + "\nD=M\n@" + str(
                    index) + "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
        elif segment == "pointer":
            if index == 0:
                address = "THIS"
                self.write(
                    "@" + address + "\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            if index == 1:
                address = "THAT"
                self.write(
                    "@" + address + "\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def pop_static_segment(self, index):
        """
        write the assembly code that is the translation of "pop static index" command
        """
        address = str(16 + index)
        self.write(
            "@" + address + "\nD=M\n@" + str(
                index) + "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def push_zero_k_times(self, k):
        for i in range(k):
            self.push_constant_segment(0)  # todo

    def write_label(self, label):
        """Writes assembly code that effects the label command."""
        self.write("(" + label + ")\n")
        # write (label_name)

    def write_goto(self, label):
        """Writes assembly code that effects the goto command."""
        self.write("@" + label + "\n0;JMP\n")
        # @ f$label_name
        # 0:JMP
        #

    def write_if(self, label):
        """Writes assembly code that effects the if-goto command."""
        self.write("@SP\nD=M\n@" + label + "\nD;JNE\n")
        # @SP
        # D=M
        # @ f$label LABEL
        # D:JNE
        #

    def write_call(self, function_name, num_args):
        """Writes assembly code that effects the call command."""
        num = self.new_return_num()
        return_address = "return_address"+str(num)
        self.push_label("THAT")
        self.push_label("LCL")
        self.push_label("ARG")
        self.push_label("THIS")
        self.push_label("THAT")
        self.label_eq_label_minus_constant("ARG","SP",num_args+5)
        self.label_eq_label("LCL","SP")
        self.write_goto(function_name)
        self.write_label(return_address)

    def write_return(self):
        """Writes assembly code that effects the return command."""
        # todo
        # self.label_eq_label("R13","LCL")
        # self.label_eq_label("R13","LCL")
        #
        #
        #
        #
        #

    def write_function(self, function_name, num_locals):
        """Writes assembly code that effects the function command."""

    def write_init(self, label):
        """Writes bootstrap code"""

    def label_eq_constant(self, label, constant):
        """Writes assmebly for label=constant"""
        self.write("@" + str(constant) + "\nD=A\n@" + label + "\nM=D\n")
        # @constant
        # D=A
        # @label
        # M=D

    def label_eq_label(self, label1, label2):
        """Writes assmebly for label1=label2"""
        self.write("@" + label2 + "\nD=A\n@" + label1 + "\nM=D\n")
        # @label2
        # D=A
        # @label1
        # M=D

    def label_eq_label_minus_constant(self, label1, label2, constant):
        """Writes assmebly for label=*(label2-constant)"""
        self.write("@" + label2 + "\nD=A\n@" + label1 + "\nM=D\n")
        self.label_eq_label("R15",label2)
        self.label_eq_constant("R14", constant)
        # @R15
        # D=M
        # @R14
        # D=D-A
        # @label1
        # M=D
        self.write("@R15\nD+M\n@R14\nD=D-A\n@"+label1+"\nM+D\n")
        # todo without registers for safety
        # todo recheck logic

    def push_label(self, label):
        """Writes assmebly for push adress of label to stack"""
        self.write("@" + label + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # @label
        # D=M
        # @SP
        # A=M
        # M=D
        # @SP
        # M=M+1

    def write(self, string):
        """
        close an output file
        """
        self.__file.write(string)

    def new_return_num(self):
        num = self.__return_num
        self.__return_num +=1
        return num


    def close(self):
        """
        close an output file
        """
        self.__file.close()
