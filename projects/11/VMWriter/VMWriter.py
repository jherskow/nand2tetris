##########################################################################
# FILE : VMWriter.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex11 2017-2018
# DESCRIPTION:
##########################################################################



class VMWriter:
    """Emits VM commands into a file, using the VM command syntax."""

    def __init__(self, output_file):
        """
        Creates a new file and prepares it for writing.
        """
        self.output_file = output_file

    def write_push(self, segment, index):
        """Writes a VM push command."""
        self.output_file.write("push " + str(segment) + " " + str(index) + "\n")

    def write_pop(self, segment, index):
        """Writes a VM pop command."""
        self.output_file.write("push " + str(segment) + " " + str(index) + "\n")

    def write_arithmetic(self, command):
        """Writes a VM arithmetic command."""
        self.output_file.write(command + "\n")

    def write_label(self, label):
        """Writes a VM label command."""
        self.output_file.write("label " + label + "\n")

    def write_goto(self, label):
        """Writes a VM goto command."""
        self.output_file.write("goto " + label + "\n")

    def write_if(self, label):
        """Writes a VM if-goto command."""
        self.output_file.write("if-goto " + label + "\n")

    def write_call(self, name, n_args):
        """Writes a VM call command."""
        self.output_file.write("call " + str(name) + " " + str(n_args) + "\n")

    def write_function(self, name, n_locals):
        """Writes a VM function command."""
        self.output_file.write("function " + str(name) + " " + str(n_locals) + "\n")

    def write_return(self):
        """Writes a VM return command."""
        self.output_file.write("return" + "\n")

    def write(self, string):
        """Writes a string directly. NO NEWLINE!"""
        self.output_file.write(string)

    def close(self):
        """Closes the output file."""
        self.output_file.close()
