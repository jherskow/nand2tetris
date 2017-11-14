##########################################################################
# FILE : Assembler.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# EXERCISE : nand2tetris ex3 2017-2018
# DESCRIPTION: Assembler for hack
##########################################################################

comps = {
    "0": "1110101010",
    "1": "1110111111",
    "-1": "1110111010",
    "D": "1110001100",
    "A": "1110110000",
    "M": "1111110000",
    "!D": "1110001101",
    "!A": "1110110001",
    "!M": "1111110001",
    "-D": "1110001111",
    "-A": "1110110011",
    "-M": "1111110011",
    "D+1": "1110011111",
    "A+1": "1110110111",
    "M+1": "1111110111",
    "D-1": "1110001110",
    "A-1": "1110110010",
    "M-1": "1111110010",
    "D+A": "1110000010",
    "D+M": "1111000010",
    "D-A": "1110010011",
    "D-M": "1111010011",
    "A-D": "1110000111",
    "M-D": "1111000111",
    "D&A": "1110000000",
    "D&M": "1111000000",
    "D|A": "1110010101",
    "D|M": "1111010101",
    # todo ensure correct - do others not matter??
    "D<<": "1010110000",
    "A<<": "1010100000",
    "M<<": "1011100000",
    "D>>": "1010010000",
    "A>>": "1010000000",
    "M>>": "1011000000",
}

dests = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jumps = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

predefs = {
    "SP":"000000000000000",
    "LCL":"000000000000001",
    "ARG":"000000000000010",
    "THIS":"000000000000011",
    "THAT":"000000000000100",
    "R0":"000000000000000",
    "R1":"000000000000001",
    "R2":"000000000000010",
    "R3":"000000000000011",
    "R4":"000000000000100",
    "R5":"000000000000101",
    "R6":"000000000000110",
    "R7":"000000000000111",
    "R8":"000000000001000",
    "R9":"000000000001001",
    "R10":"000000000001010",
    "R11":"000000000001011",
    "R12":"000000000001100",
    "R13":"000000000001101",
    "R14":"000000000001110",
    "R15":"000000000001111",
    "SCREEN": "100000000000000",
    "KBD": "110000000000000"
}
