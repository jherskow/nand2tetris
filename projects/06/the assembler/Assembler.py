##########################################################################
# FILE : Assembler.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# EXERCISE : nand2tetris ex3 2017-2018
# DESCRIPTION: Assembler for hack
##########################################################################
import symbol_table as sym
import sys

# ========= constants =============
COMMENT_DELIM = '//'
NEWLINE = '\n'
STRUDEL = '@'
OPEN_BRACKET = '('
CLOSED_BRACKET = ')'
EQUAL = '='
SEMICOLON = ';'
EMPTY_3_BIT = '000'
C_CODE = '111'
A_CODE = '0'
MAX_ROM = 32767
MAX_ADDRESS = 24576

# ========= GLOBALS =============
variable_counter = 16
var_table = {}
out_array = []


# ========= main =============

def main():
    """
    Does the real work around here
    """

    filename = sys.argv[1]  # todo directory option
    assemble(filename)


def assemble(filename):
    """

    :param filename:
    :return:
    """

    global variable_counter
    global var_table
    global out_array
    variable_counter = 16
    var_table = {}
    out_array = []

    var_table.update(sym.predefs)

    in_array = read_input(filename)

    make_labels(in_array)

    for line in in_array:
        parse_line(line)

    write_output(filename)

    # todo debug
    print("done!")

    return 0


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

            # remove comments
            line = line.split(COMMENT_DELIM)
            line = line[0]

            # remove whitespace
            line = line.strip()

            # add line if not empty
            if line != "":
                lines.append(line)

    file.close()

    return lines


# output prep#####################
def write_output(filename):
    global out_array

    # make output name #todo make func
    filename = filename.split(".")
    filename = filename[0]
    filename = filename + ".hack"

    with open(filename, 'w') as file:
        for i, line in enumerate(out_array):
            file.write(out_array[i])
    file.close()


# #assembly######################################################


def make_labels(lines):
    i = 0

    for line in lines:
        if line.startswith(OPEN_BRACKET):
            line = line.split(CLOSED_BRACKET)[0]
            line = line.split(OPEN_BRACKET)[1]
            var_table[line] = to_bin_15(i)
        elif line.startswith(STRUDEL):
            i += 1
        elif EQUAL in line or SEMICOLON in line:
            i += 1


def parse_line(line):
    global out_array

    if line.startswith(OPEN_BRACKET):
        return
    elif line.startswith(STRUDEL):
        out_line = parse_a_instruction(line)
    else:
        out_line = parse_c_instruction(line)
    out_array.append(out_line)


def parse_a_instruction(line):
    # todo
    value = line.split(STRUDEL)[1]
    if value.isdigit():
        replace = to_bin_15(int(value))
    elif value in var_table:
        replace = var_table[value]
    else:
        replace = var_table[value] = allocate_ram()
    out_line = "0" + replace + NEWLINE
    return out_line


def parse_c_instruction(line):
    try:
        if EQUAL in line and SEMICOLON in line:
            dest, rest = line.split(EQUAL)
            comp, jump = rest.split(SEMICOLON)
            dest = sym.dests[dest]
            comp = sym.comps[comp]
            jump = sym.jumps[jump]

        elif EQUAL in line:
            dest, comp = line.split(EQUAL)
            dest = sym.dests[dest]
            comp = sym.comps[comp]
            jump = EMPTY_3_BIT

        elif SEMICOLON in line:
            comp, jump = line.split(SEMICOLON)
            dest = EMPTY_3_BIT
            comp = sym.comps[comp]
            jump = sym.jumps[jump]

        else:
            print("unresolvable C instruction - unknown command type")
            raise SystemExit

    except KeyError:
        print("unresolvable C instruction - variable not found")
        raise SystemExit

    except ValueError:
        print("unresolvable C instruction - bad syntax")
        raise SystemExit

    out_line = C_CODE + comp + dest + jump + NEWLINE
    return out_line


def to_bin_15(num):
    # if num >= MAX_ROM:
    #    print("15 bit binary overflow")
    #    raise SystemExit  #todo check
    return format(num, '015b')


def allocate_ram():
    global variable_counter
    if variable_counter > MAX_ADDRESS:
        print("memory full")
        raise SystemExit
    address = format(variable_counter, '015b')
    variable_counter += 1
    return address


# todo test code ###################################

assemble("/cs/usr/jherskow/HUJI/nand2tetris/projects/06/pong/Pong.asm")
