import re
import sys
import os
import CodeWriter

ASM_EXTENSION = ".asm"


class Parser:
    arithmeticCommands = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}

    def __init__(self, input_file):
        self.__file_path = input_file
        self.__file = open(input_file, "r")
        self.__current_line = None

    def get_curent_line(self):
        return self.__current_line

    def has_more_commands(self):
        """
        method that check if there are more commands in the input file.
        """
        self.__current_line = self.__file.readline()
        return bool(self.__current_line)

    def advance(self):
        """ method that reads the next command from the input and makes it the current command"""
        if self.has_more_commands():
            self.__current_line = self.__file.readline()

    def remove_comments(self, line):
        line = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", line)
        # remove all occurance streamed comments (/*COMMENT */) from string
        line = re.sub(re.compile("//.*?\n"), "\n", line)
        # remove all occurance singleline comments (//COMMENT\n ) from string
        return line

    def clean_file_comments(self):
        """
        clean the file from comments and white spaces
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
        if split_line[0] in Parser.arithmeticCommands:
            return "C_ARITHMETIC"
        elif split_line[0] == "push":
            return "C_PUSH"
        elif split_line[0] == "pop":
            return "C_POP"
        elif split_line[0] == "label":
            return "C_LABEL"
        elif split_line[0] == "goto":
            return "C_GOTO"
        elif split_line[0] == "if":
            return "C_IF"
        elif split_line[0] == "function":
            return "C_FUNCTION"
        elif split_line[0] == "return":
            return "C_RETURN"
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
        self.__file.close()


def get_file_name(file_path):
    base = os.path.basename(file_path)
    os.path.splitext(base)
    return os.path.splitext(base)[0]


def parse_file_to_write(parser, codeWriter):
    parser.remove_file_comments()
    while parser.has_more_commands():
        type = parser.command_type()
        if type == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parser.arg1())

        elif type == "C_PUSH" or type == "C_POP":
            codeWriter.writePushPop(type, parser.arg1(), parser.arg2())


def read_file(file_path, writer):
    parser = Parser(file_path)
    parse_file_to_write(parser, writer)
    parser.close_file()


def read_dir(dir_path, writer):
    for f in os.listdir(dir_path):
        if f.endswith(".vm"):
            read_file(dir_path + "/" + f, writer)
    writer.close()


def main():
    if len(sys.argv) != 2:
        print("USAGE: VMEmulator ~directory")
        return exit(1)
    if os.path.isfile(sys.argv[1]):
        writer = CodeWriter.CodeWriter(sys.argv[1].split(".")[0] + ASM_EXTENSION)
        read_file(sys.argv[1], writer)
        writer.close()

    if os.path.isdir(sys.argv[1]):
        file_name = get_file_name(sys.argv[1])
        writer = CodeWriter.CodeWriter(sys.argv[1] +"/"+ file_name + ASM_EXTENSION)
        read_dir(sys.argv[1], writer)


if __name__ == '__main__':
    main()
