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
BIN_15 = '015b'
A_CODE = '0'
NULL = 'null'
MAX_ROM = 32767
MAX_ADDRESS = 24576

# ========= globals =============
variable_counter = 16
var_table = {}
out_array = []


# ========= main =============

def main():
    """
    Does the real work around here
    """

    filename = sys.argv[1]  # todo directory option??
    assemble(filename)


def assemble(filename):
    """

    :param filename:
    :return:
    """

    global variable_counter
    global var_table
    global out_array

    # re-initialise global variables
    variable_counter = 16
    var_table = {}
    out_array = []
    var_table.update(sym.predefs)


    in_array = read_input(filename)

    make_labels(in_array)
    i=1 # todo remove
    for line in in_array:
        print("line "+str(i), end='....')
        parse_line(line)
        print(str(i)+" done")
        i+=1

    write_output(filename)

    print("done!")

    return 0

# ========= input prep =============

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

# ========= output prep =============

def write_output(filename):
    global out_array

    # make output name
    out_name = filename.split(".")[0] + ".hack"

    with open(out_name, 'w') as file:
        for i, line in enumerate(out_array):
            file.write(out_array[i])
    file.close()

# ========= assembly=============


def make_labels(lines):
    i = 0

    for line in lines:
        if line.startswith(OPEN_BRACKET):
            line = line.split(CLOSED_BRACKET)[0]
            line = line.split(OPEN_BRACKET)[1]
            var_table[line] = to_bin_15(i)
        else:
            i=i+1


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

    equal = EQUAL in line
    semicolon = SEMICOLON in line
    try:
        if equal and semicolon: # dest=comp;jump
            dest, rest = line.split(EQUAL)
            comp, jump = rest.split(SEMICOLON)

        elif equal and not semicolon: # dest=comp
            dest, comp = line.split(EQUAL)
            jump = NULL

        elif semicolon and not equal: # comp;jmp
            comp, jump = line.split(SEMICOLON)
            dest = NULL

        else: # comp
            comp = line
            jump = NULL
            dest = NULL

        # parse commands using table
        dest = sym.dests[dest.strip()]
        comp = sym.comps[comp.strip()]
        jump = sym.jumps[jump.strip()]

        # todo check whitespace compatability

    # todo remove all exceptions before submission
    except KeyError:
        print("unresolvable C instruction - variable not found")
        raise SystemExit

    except ValueError:
        print("unresolvable C instruction - bad syntax")
        raise SystemExit

    out_line = comp + dest + jump + NEWLINE
    return out_line


def to_bin_15(num):
    return format(num, BIN_15)

def allocate_ram():
    global variable_counter
    # get address
    address = to_bin_15(variable_counter)
    # and increment the counter after!
    variable_counter += 1
    return address


# todo test code ###################################

assemble("/home/jjherskow/HUJI/nand2tetris/projects/06/myPong/Pong.asm")

# todo  - If semicilon is indicative- only test trim and standalone computation
# if not indicative - must inclde all -and test trim

