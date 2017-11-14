##########################################################################
# FILE : Assembler.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# EXERCISE : nand2tetris ex3 2017-2018
# DESCRIPTION: Assembler for hack
##########################################################################
import symbol_table as sym


# ========= constants =============
COMMENT_DELIM = '//'
NEWLINE = '\n'
STRUDEL = '@'
BRACKET = '('

# counters
symbol_counter = 16

# dicts
var_table = {}

# input prep#####################

def read_input(filename):
    """
    Converts text file into array of strings
    :param filename: text file of compatible format
    :return: string array
    """

    lines = []

    with open(filename) as file:
        for line in file:

            # remove whitespace
            line = line.strip()

            # remove comments
            line = line.split(COMMENT_DELIM)
            line = line[0]

            # add line if not empty
            if line != "":
                lines.append(line)

    file.close()

    return lines


# output prep#####################
def write_output(filename, line_array):
    # make output name #todo make func
    filename = filename.split(".")
    filename = filename[0]
    filename = filename + ".hack"

    with open(filename, 'w') as file:
        for i, line in enumerate(line_array):
            file.write(line_array[i] + NEWLINE)
    file.close()

    return 0


##assembly######################################################


####
def make_labels(lines):
    for line in lines:
        if line.startswith(BRACKET):
            line = line.split(")")[0]
            line = line.split("(")[1]
            address = to_binary(symbol_counter)
            var_table[line]=address
            symbol_counter+=1;


def parseLine(line):
    if line.startswith(STRUDEL):
        parse_a_instruction(line)
    elif line.startswith(BRACKET):
        pass
    else:
        parse_c_instruction(line)


def parse_a_instruction(line):
    # todo
    return 0


def parse_c_instruction(line):
    # todo
    return 0


def assign_symbol(line):
    # todo
    return 0

def to_binary(num):
    return "{0:b}".format(num)



    # prep input
    # assign symbolic refences
    # go again and translate to binary
    #


    # func assign adress - assigns a symbol to a memory register dictionary in ascending order
