C_PUSH = "push"
C_POP = "pop"


class CodeWriter:
    arithmeticCommands = {"add", "sub", "neg", "eq", "gt", "lt", "and",
                          "or", "not"}
    segments = {"local": "LCL", "argument": "ARG", "this": "THIS",
                "that": "THAT"}

    def __init__(self, out_filepath):
        self.__file = open(out_filepath, 'w')
        self.__label_num = 0  # counter of labels number
        self.__return_num_counter = 0  # counter of labels number
        self.__cur_filename = ""
        self.__in_function_def = False
        self.__function_name = ""
        # self.write_init() #todo put when necessary


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
        self.write("@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\n@CONDITION" + str(
            self.__label_num) + "\n" +
                   "D;" + "JEQ" + "\n@SP\nA=M-1\nM=0\n@CONTINUE" + str(
            self.__label_num) + "\n0;JMP\n(CONDITION" +
                   str(
                       self.__label_num) + ")\n@SP\nA=M-1\nM=-1\n(CONTINUE" + str(
            self.__label_num) + ")\n")

    def gt_command(self):
        """
               write assembly code that is equivalent to a gt comparision command
         """
        self.write(
            "@SP\nA=M-1\nD=M\n@NEG1" + str(
                self.__label_num) + "\nD;JLT\n@POS1" + str(
                self.__label_num) +
            "\nD;JGE\n(NEG1" + str(
                self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@POS2" + str(
                self.__label_num) + "\nD;JGT\n@CONT"
            + str(self.__label_num) + "\n0;JMP\n(POS1" + str(
                self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@NEG2" +
            str(self.__label_num) + "\nD;JLT\n@CONT" + str(
                self.__label_num) + "\n0;JMP\n(POS2" + str(
                self.__label_num) + ")\n@SP"
                                    "\nA=M-1\nA=A-1\nM=-1\n@SP\nM=M-1\n@ENDLABEL" + str(
                self.__label_num) + "\n0;JMP\n(NEG2" + str(
                self.__label_num) + ")\n@SP" +
            "\nA=M-1\nA=A-1\nM=0\n@SP\nM=M-1\n@ENDLABEL" + str(
                self.__label_num) + "\n0;JMP\n(CONT" + str(
                self.__label_num) + ")\n"
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
            "@SP\nA=M-1\nD=M\n@NEG1" + str(
                self.__label_num) + "\nD;JLT\n@POS1" + str(
                self.__label_num) +
            "\nD;JGE\n(NEG1" + str(
                self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@POS2" + str(
                self.__label_num) + "\nD;JGT\n@CONT"
            + str(self.__label_num) + "\n0;JMP\n(POS1" + str(
                self.__label_num) + ")\n@SP\nA=M-1\nA=A-1\nD=M\n@NEG2" +
            str(self.__label_num) + "\nD;JLT\n@CONT" + str(
                self.__label_num) + "\n0;JMP\n(POS2" + str(
                self.__label_num) + ")\n@SP"
                                    "\nA=M-1\nA=A-1\nM=0\n@SP\nM=M-1\n@ENDLABEL" + str(
                self.__label_num) + "\n0;JMP\n(NEG2" + str(
                self.__label_num) + ")\n@SP" +
            "\nA=M-1\nA=A-1\nM=-1\n@SP\nM=M-1\n@ENDLABEL" + str(
                self.__label_num) + "\n0;JMP\n(CONT" + str(
                self.__label_num) + ")\n"
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
            self.push_lcl_arg_this_that_segments(
                CodeWriter.segments.get(segment), index)
        if segment == "temp" or segment == "pointer":
            self.push_pointer_temp_segments(segment, index)
        if segment == "static":
            self.push_static_segment(index)

    def push_constant_segment(self, index):
        """ write the assembly code that is the translation of  "push constant index" command"""
        self.write("@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_static_segment(self, index):
        """ write the assembly code that is the translation of "push static index " command"""
        # address = str(16 + int(index))
        # todo check correct segment & remove address line above me
        self.write("@" + self.__cur_filename + "." + str(index) + "\nD=M\n@" + str(
            index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_lcl_arg_this_that_segments(self, segment, index):
        """
        write the assembly code that is translation of "push (local\argument\this\that) index" command
        """
        self.write("@" + segment + "\nD=M\n@" + str(
            index) + "\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def push_pointer_temp_segments(self, segment, index):
        """
        write the assembly code that is translation of "push (pointer\temp) index" command
        """
        if segment == "temp":
            ram_address = index +5
            self.write(
                # @place //point to ram[i+5]
                # D=M // put value in D
                # @SP // look at SP
                # A=M // Put number of SP in A
                # M=D //put value there
                # @SP // look at Sp
                # M=M+1 increase SP by one
                "@"+ram_address+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1")


        elif segment == "pointer":
            ram_address = index + 3
            self.write(
                # @place //point to ram[i+5]
                # D=M // put value in D
                # @SP // look at SP
                # A=M // Put number of SP in A
                # M=D //put value there
                # @SP // look at Sp
                # M=M+1 increase SP by one
                "@" + ram_address + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1")

    def pop_command(self, segment, index):
        """
        write the assembly code that translation of pop command
        """
        if segment in CodeWriter.segments:
            self.pop_lcl_arg_this_that_segments(
                CodeWriter.segments.get(segment), index)
        elif segment == "temp" or segment == "pointer":
            self.pop_temp_pointer_segments(segment, int(index))
        elif segment == "static":
            self.pop_static_segment(index)

    def pop_lcl_arg_this_that_segments(self, segment, index):
        """
        write the assembly code that translation of "pop (local\argument\this\that) index" command
        """
        self.write(
            "@" + segment + "\nD=M\n@" + str(index) +
            "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def pop_temp_pointer_segments(self, segment, index):
        """
        write the assembly code that translation of "pop (temp\pointer) index" command
        """
        if segment == "temp":
            ram_address = index + 5
            self.write(
                # @SP
                # MA=M-1 // deacrease SP and A to see top of stack
                # D=M //d has the value at top of stack
                # @place //point to ram[i+5]
                # M=D //put value there #todo check correctness
                "@SP\nMA=M-1\nD=M\n@"+ram_address+"\nM=D\n")
        elif segment == "pointer":
            ram_address = index + 3
            self.write(
                # @SP
                # MA=M-1 // deacrease SP and A to see new top of stack
                # D=M //d has the value at top of stack
                # @place //point to ram[i+3]
                # M=D //put value there
                "@SP\nMA=M-1\nD=M\n@"+ram_address+"\nM=D\n")

    def pop_static_segment(self, index):
        """
        write the assembly code that is the
        translation of "pop static index" command
        """
        # address = str(16 + index)
        # todo check correct segment & remove address line above me
        self.write\
            ("@" + self.__cur_filename + "." + str(index) + "\nD=M\n@" +
             str(index) +
                "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def push_zero_k_times(self, k):
        for i in range(k):
            self.push_constant_segment(0)

    def write_label(self, label):
        """Writes assembly code that effects the label command."""
        label = self.label_by_scope(label)
        self.write("(" + label + ")\n")
        # write (label_name)

    def write_goto(self, label):
        """Writes assembly code that effects the goto @label command."""
        label = self.label_by_scope(label)
        self.write("@" + label + "\n0;JMP\n")
        # @label
        # 0:JMP
        #

    def write_if(self, label):
        """Writes assembly code that effects the if-goto command."""
        label=self.label_by_scope(label)
        self.write("@SP\nMA=M-1\nD=M\n@" + label + "\nD;JNE\n")
        # @SP
        # MA=M-1 // decrease SP
        # D=M /Put value in D
        # @label
        # D:JNE
        #

    def write_call(self, function_name, num_args):
        """Writes assembly code that effects the calling a function."""
        return_num = self.new_return_num()
        return_address = self.__cur_filename + "_ret_" + str(return_num)
        self.push_label(return_address)
        self.push_label("THAT")
        self.push_label("LCL")
        self.push_label("ARG")
        self.push_label("THIS")
        self.push_label("THAT")
        self.label_eq_label_minus_num("ARG", "SP", (int(num_args)+5))
        self.label_eq_label("LCL", "SP")
        self.write_goto(function_name)
        self.write_label(return_address)

    def write_function(self, function_name, num_locals):
        """Writes assembly code that effects a function def start."""
        self.__function_name = function_name
        self.write_label(function_name)
        self.__in_function_def = True
        self.push_zero_k_times(int(num_locals))

    def write_return(self):
        """Writes assembly code that effects
        the return command in a func def."""
        # FRAME is R13
        self.label_eq_label("R13","LCL")
        # RET is R14
        self.label_eq_label_minus_num("R14", "R13", 5)

        # todo - *ARG = pop()  - pop value to ARG (actual arg pointer value)
        self.write("@SP\nA=A-1\nD=M\n@ARG\nM=D\n@SP\nM=M-1\n")
        # @SP
        # A=A-1
        # D=M
        # @ARG
        # M=D
        # @SP
        # M=M-1
        # todo is this ok??

        # todo check that negative const works
        self.label_eq_label_minus_num("SP", "ARG", -1)


        self.label_eq_label_minus_num("THAT", "R13", 1)
        self.label_eq_label_minus_num("THIS", "R13", 2)
        self.label_eq_label_minus_num("ARG", "R13", 3)
        self.label_eq_label_minus_num("LCL", "R13", 4)
        self.__in_function_def = False
        self.write_goto("R14")


    def write_init(self):
        """Writes bootstrap code"""
        # todo check
        self.write\
            ("@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)

    def label_eq_constant(self, label, constant):
        """Writes assembly for label=constant"""
        self.write\
            ("@" + str(constant) + "\nD=A\n@" + label + "\nM=D\n")
        # @constant
        # D=A
        # @label
        # M=D

    def label_eq_label(self, label1, label2):
        """Writes assembly for label1=label2"""
        self.write\
            ("@" + label2 + "\nD=A\n@" + label1 + "\nM=D\n")
        # @label2
        # D=A
        # @label1
        # M=D

    def label_eq_label_minus_num(self, label1, label2, num):
        """Writes assembly for label=*(label2-constant)"""
        # @label2
        # D=A
        # @str(constant)
        # D=D-A
        # @label1
        # M=D
        self.write\
            ("@"+label2+"\nD=A\n@"+str(num)+"\nD=D-A\n@"+label1+"\nM=D\n")

    def push_label(self, label):
        """Writes assembly to push ram address of label to stack"""
        self.write("@" + label + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # @label
        # D=M
        # @SP
        # A=M
        # M=D
        # @SP
        # M=M+1

    def set_cur_filename(self, filename):
        self.__cur_filename = filename

    def write(self, string):
        """
        short form for file write
        """
        self.__file.write(string)

    def new_return_num(self):
        num = self.__return_num_counter
        self.__return_num_counter += 1
        return num

    def label_by_scope(self,label):
        if self.__in_function_def:
           label = self.__function_name+"$"+label
        return label

    def close(self):
        """
        close an output file
        """
        self.__file.close()
