##########################################################################
# FILE : VMWriter.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex11 2017-2018
# DESCRIPTION:
##########################################################################



class VMWriter:
    """Emits VM commands into a file, using the VM command syntax."""


    def __init__(self,output_file):
        """
        Creates a new file and prepares it for writing.
        """

    def write_push(self,segment, index):
        """Writes a VM push command."""


    def write_pop(self,segment, index):
        """Writes a VM pop command."""

    def write_arithmetic(self,command):
        """Writes a VM arithmetic command."""


    def write_label(self,label):
        """Writes a VM label command."""


    def write_goto(self,label):
        """Writes a VM goto command."""


    def write_if(self,label):
        """Writes a VM if-goto command."""

    def write_call(self,name,n_args):
        """Writes a VM call command."""

    def write_function(self,name, n_locals):
        """Writes a VM function command."""

    def write_return(self):
        """Writes a VM return command."""

    def close(self):
        """Closes the output file."""