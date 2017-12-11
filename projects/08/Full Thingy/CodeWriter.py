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
        self.__function_name = ""
        #self.write_init() #todo put when necessary


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
            ram_address = str(index +5)
            self.write(
                # @place //point to ram[i+5]
                # D=M // put value in D
                # @SP // look at SP
                # A=M // Put number of SP in A
                # M=D //put value there
                # @SP // look at Sp
                # M=M+1 increase SP by one
                "@"+ram_address+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")


        elif segment == "pointer":
            ram_address = str(index + 3)
            self.write(
                # @place //point to ram[i+5]
                # D=M // put value in D
                # @SP // look at SP
                # A=M // Put number of SP in A
                # M=D //put value there
                # @SP // look at Sp
                # M=M+1 increase SP by one
                "@" + ram_address +"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

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
            ram_address = str(index + 5)
            self.write(
                # @SP
                # AM=M-1 // deacrease SP and A to see top of stack
                # D=M //d has the value at top of stack
                # @place //point to ram[i+5]
                # M=D //put value there
                "@SP\nAM=M-1\nD=M\n@"+ram_address+"\nM=D\n")
        elif segment == "pointer":
            ram_address = str(index + 3)
            self.write(
                # @SP
                # AM=M-1 // deacrease SP and A to see new top of stack
                # D=M //d has the value at top of stack
                # @place //point to ram[i+3]
                # M=D //put value there
                "@SP\nAM=M-1\nD=M\n@"+ram_address+"\nM=D\n")

    def pop_static_segment(self, index):
        """
        write the assembly code that is the
        translation of "pop static index" command
        """
        self.write("@" + self.__cur_filename + "." + str(index) + "\nD=M\n@" +
             str(index) +
                "\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def close(self):
        """
        close an output file
        """
        self.__file.close()


# todo ////////////////////////    MY STUFF      ////////////////////////////////////////////////


    def push_zero_k_times(self, k):
        for i in range(k):
            self.push_constant_segment(0)

    def make_unscoped_label(self, label):
        """Writes assembly code that effects the label command."""
        #if "." not in label:
         #   label = self.__cur_filename + "." + label  #todo figure out func names
        self.write("(" + label + ")\n")
        # write (label_name)

    def make_scoped_label(self, label):
        """Writes assembly code that effects the label command."""
        label = self.label_by_scope(label)
        self.write("(" + label + ")\n")
        # write (label_name)

    def write_goto_in_func(self, label):
        """Writes assembly code that effects the goto @label command."""
        label = self.label_by_scope(label)
        self.write("@" + label + "\n0;JMP\n")
        # @label
        # 0;JMP

    def write_if(self, label):
        """Writes assembly code that effects the if-goto command."""
        label=self.label_by_scope(label)
        self.pop_stack_to_d()
        self.write("@" + label + "\nD;JNE\n")

        # todo (stuff beneath is old)
        # @SP
        # AM=M-1 // decrease SP
        # D=M /Put value in D
        # @label
        # D;JNE
        #

    def write_call(self, function_name, num_args):
        """Writes assembly code that effects the calling a function."""
        return_num = self.new_return_num()
        return_address = self.__cur_filename + "_ret_" + str(return_num)

        # push @return adress
        self.push_address(return_address)

       # push lcl
        self.push_value("LCL")
        # push lcl
        self.push_value("ARG")
        # push lcl
        self.push_value("THIS")
        # push lcl
        self.push_value("THAT")

        # arg = (SP -n -5)
        self.val_label_eq_val_label_minus_num("ARG","SP",(int(num_args)+5))

        #lcl = SP
        self.val_pointer_eq_val_pointer("LCL", "SP")

        #goto(function_name)
        self.write("@"+function_name+"\n0;JMP\n")
        self.make_unscoped_label(return_address)

    def write_function(self, function_name, num_locals):
        """Writes assembly code that effects a function def start."""
        self.__function_name = function_name
        self.make_unscoped_label(function_name)
        self.push_zero_k_times(int(num_locals))


    def write_return(self):
        """Writes assembly code that effects
        the return command in a func def."""


        # FRAME is R13
        self.val_pointer_eq_val_pointer("R13", "LCL")

        # RET is R14
        self.val_pointer_eq_val_at_pointer_minus_num("R14", "R13", 5)

        # *ARG = pop()  - pop value from stack to where ARG is pointing
        self.pop_stack_to_d()
        self.d_to_pointed_value("ARG")

        # todo old -----------------------------------
        # # *ARG = pop()  - pop value from stack to where ARG is pointing
        # self.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        # # @SP    // A is adressof sp
        # # AM=M-1   //A is adressof top stack val, SP--  #todo fixed?
        # # D=M    // D is top stack val
        # # @ARG    // A is arg pointer
        # # A=M     // a is spot pointed by ARG
        # # M=D    // value where ARG is pointing is now top stack val
        # todo old -----------------------------------


        # SP=ARG+1
        self.val_label_eq_val_label_plus_num("SP", "ARG", 1)


        self.val_pointer_eq_val_at_pointer_minus_num("THAT", "R13", 1)
        self.val_pointer_eq_val_at_pointer_minus_num("THIS", "R13", 2)
        self.val_pointer_eq_val_at_pointer_minus_num("ARG", "R13", 3)
        self.val_pointer_eq_val_at_pointer_minus_num("LCL", "R13", 4)

        # goto R14(RET)
        self.write("@R14\n0;JMP\n")


    def write_init(self):
        """Writes bootstrap code"""
        # todo check
        self.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)

    def val_pointer_eq_val_pointer(self, label1, label2):
        """Writes assembly for label1=label2"""
        # put label2's value in D
        self.value_to_d(label2)
        # put D in label 1
        self.d_to_value(label1)

        # todo (stuff beneath is old)
        # self.write\
        #     ("@" + label2 + "\nD=M\n@" + label1 + "\nM=D\n")
        # @label2
        # D=M     // d is value of pinter2
        # @label1
        # M=D     // pointer1 now has this value

    def val_pointer_eq_val_at_pointer_minus_num(self, label1, label2, pos_num):
        """Writes assembly for label=*(label2-constant) (value at num before pointe by lab2)"""
        # put label2's value in D
        self.value_to_d(label2)

        # remove number from D
        self.write("@"+str(pos_num)+"\nD=D-A\n")

        # A=D // A = label2 - num
        # D=M   // and save RAM[label2 - num] to D
        self.write("A=D\nD=M\n")

        # put D in label 1
        self.d_to_value(label1)

        # todo (stuff beneath is old)
        # @LCL
        # D=M   //d has value of LCL
        # @str(num)
        # A=D-A  // A has LCL-num
        # D=M  // D has the value at ram[LCL-num]
        # @label1
        # M=D     // label one now has this value
        # self.write\
        #     ("@" + label2 +"\nD=M\n@" + str(pos_num) + "\nA=D-A\nD=M\n@" + label1 + "\nM=D\n")

    def val_label_eq_val_label_plus_num(self, label1, label2, pos_num):
        """Writes assembly for label=label2+constant """
        self.value_to_d(label2)
        # add number to D
        self.write("@"+str(pos_num)+"\nD=D+A\n")
        self.d_to_value(label1)

        # todo (stuff beneath is old)
        # @ARG
        # D=M   // d has the value of ARG
        # @str(num)
        # D=D+A  // d has ARG+num
        # @label1
        # M=D // label1= ARG+num
        #self.write\
        #    ("@" + label2 +"\nD=M\n@" + str(pos_num) + "\nD=D+A\n@" + label1 + "\nM=D\n")

    def val_label_eq_val_label_minus_num(self,label1,label2,pos_num):
        self.value_to_d(label2)
        # remove number from D
        self.write("@"+str(pos_num)+"\nD=D-A\n")
        # place in label 1
        self.d_to_value(label1)



    def push_address(self, label):
        """Writes assembly to push number saved in label to stack"""
        self.address_to_d(label)
        self.push_d_to_stack()

    def push_value(self, label):
        """Writes assembly to push number saved in label to stack"""
        self.value_to_d(label)
        self.push_d_to_stack()

    def push_pointed_value(self, label):
        """Writes assembly to push number saved in label to stack"""
        self.pointed_value_to_d(label)
        self.push_d_to_stack()


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
        label = self.__function_name+"$"+label
        return label



 # todo //////// new idea

    def push_d_to_stack(self):
        self.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # @SP      A is adresss of SP (ram[0])
        # A=M    // A is address of stack head
        # M=D    // memory at stack head now has value D
        # @SP    // advance SP
        # M=M+1  //

    def pop_stack_to_d(self):
        self.write("@SP\nAM=M-1\nD=M\n")
        # @SP      A is adresss of SP (ram[0])
        # AM=M-1    // A and SP both have one less than SP's orig value
        # D=M    // D now has the value at this place

    def address_to_d(self,label):
        self.write("@"+label+"\nD=A\n")
        # @label      A is adress for label
        # D=A    // D now has this adress

    def value_to_d(self, label):
        self.write("@" + label + "\nA=M\nD=A\n")
        # @label      A is address for label
        # A=M     // a is value at label
        # D=A    // D now has this value

    def pointed_value_to_d(self, label):
        self.write("@" + label + "\nA=M\nD=M\n")
        # @label      A is adress for label
        # A=M     // a is value at label
        # D=M    // D now has the var at RAM[value]

    def d_to_pointed_value(self, label):
        self.write("@" + label + "\nA=M\nM=D\n")
        # @label      A is adress for label
        # A=M     // A is value at label
        # M=D    // RAM[value] now has the var at D

    def d_to_value(self, label):
        self.write("@" + label + "\nM=D\n")
        # @label      A is adress for label
        # M=D    // RAM[label] now has the var at D