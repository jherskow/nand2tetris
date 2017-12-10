import re
import sys
import os
import CodeWriter

ASM_EXTENSION = ".asm"


class Parser:
    arithmeticCommands = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}

    def __init__(self, in_filename):
        self.__file_path = in_filename
        self.__file = open(in_filename, "r")
        self.__current_line = None

    def get_current_line(self):
        return self.__current_line

    def has_more_commands(self):
        """
        checks if there are more commands in the input file.
        """
        self.__current_line = self.__file.readline()
        return bool(self.__current_line)

    def advance(self):
        """reads the next command to current_line"""
        if self.has_more_commands():
            self.__current_line = self.__file.readline()

    def remove_comments(self, line):
        """ removes comments from a line"""
        """line = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", line)
        # remove all occurrences of stream comments (/*COMMENT */) from string""" #todo remove

        line = re.sub(re.compile("//.*?\n"), "\n", line)
        # remove all occurrences of single line comments (//COMMENT\n ) from string
        return line

    def remove_file_comments(self):
        """
        clean the entire file from comments and white spaces
        """
        updated_file = open("temp.vm", "w")
        for line in self.__file.readlines():
            new_line = self.remove_comments(line)
            if new_line != "\n":
                updated_file.write(new_line)
        updated_file.close()
        self.__file = open(updated_file.name, "r")

    def command_type(self):
        """
        returns the type of the current VM command
        """
        split_line = self.__current_line.split()
        if split_line[0] in Parser.arithmeticCommands:  ##
            return "C_ARITHMETIC"
        elif split_line[0] == "push":
            return "C_PUSH"
        elif split_line[0] == "pop":
            return "C_POP"
        elif split_line[0] == "label":
            return "C_LABEL"
        elif split_line[0] == "goto":
            return "C_GOTO"
        elif split_line[0] == "if-goto": #todo check string
            return "C_IF"
        elif split_line[0] == "function":
            return "C_FUNCTION"
        elif split_line[0] == "return":
            return "C_RETURN"
        elif split_line[0] == "call":
            return "C_CALL"

    def arg1(self):
        if self.command_type() == "C_ARITHMETIC":
            return self.__current_line.split()[0]
        elif self.command_type() == "RETURN":
            return None
        else:
            return self.__current_line.split()[1]

    def arg2(self):
        if self.command_type() == "C_PUSH" or self.command_type() == "C_POP" or \
                        self.command_type() == "C_FUNCTION" or self.command_type() == "C_CALL":
            return self.__current_line.split()[2]
        else:
            return None

    def close_file(self):
        """closes the input file"""
        self.__file.close()


def get_file_name(file_path):
    """
    :param file_path: path to a file, including file itself
    :return:  path of the directory in which the object resides
    """
    base = os.path.basename(file_path)
    os.path.splitext(base)
    return os.path.splitext(base)[0]


def parse_file_to_write(parser, codeWriter):
    parser.remove_file_comments()
    while parser.has_more_commands():
        type = parser.command_type()
        if type == "C_ARITHMETIC":
            codeWriter.write_arithmetic(parser.arg1())
        elif type == "C_PUSH" or type == "C_POP":
            codeWriter.write_push_pop(type, parser.arg1(), parser.arg2())
        elif type == "C_LABEL":
            codeWriter.make_scoped_label(parser.arg1())
        elif type == "C_GOTO":
            codeWriter.write_goto(parser.arg1())
        elif type == "C_IF":
            codeWriter.write_if(parser.arg1())
        elif type == "C_FUNCTION":
            codeWriter.write_function(parser.arg1(), parser.arg2())
        elif type == "C_RETURN":
            codeWriter.write_return()
        elif type == "C_CALL":
            codeWriter.write_call(parser.arg1(), parser.arg2())
        # todo check


def parse_file(file_path, writer):
    parser = Parser(file_path)
    file_name = sys.argv[1].split("/")[-1].split(".")[0]
    writer.set_cur_filename(file_name)
    parse_file_to_write(parser, writer)
    parser.close_file()


def parse_dir(dir_path, writer):
    for f in os.listdir(dir_path):
        if f.endswith(".vm"):
            parse_file(dir_path + "/" + f, writer)
    writer.close()


def main():
    if len(sys.argv) != 2:
        print("USAGE: VMEmulator ~directory/file")
        return exit(1)

    abs_path = str(os.path.abspath(sys.argv[1]))

    if os.path.isfile(abs_path):
        out_filepath = abs_path.split(".vm")[0] + ASM_EXTENSION
        writer = CodeWriter.CodeWriter(out_filepath)
        parse_file(sys.argv[1], writer)
        writer.close()

    if os.path.isdir(abs_path):
        file_name = get_file_name(abs_path)
        out_filepath = abs_path +"/"+ file_name + ASM_EXTENSION
        writer = CodeWriter.CodeWriter(out_filepath)
        parse_dir(sys.argv[1], writer)


if __name__ == '__main__':
    main()
