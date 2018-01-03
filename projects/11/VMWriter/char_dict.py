##########################################################################
# FILE : char_dict.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex10 2017-2018
# DESCRIPTION:
##########################################################################

KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INT_CONST = "INT_CONST"
STRING_CONST = "STRING_CONST"

K_CLASS = "CLASS"
K_METHOD = "METHOD"
K_FUNCTION = "FUNCTION"
K_CONSTRUCTOR = "CONSTRUCTOR"
K_INT = "INT"
K_BOOLEAN = "BOOLEAN"
K_CHAR = "CHAR"
K_VOID = "VOID"
K_VAR = "VAR"
K_STATIC = "STATIC"
K_FIELD = "FIELD"
K_LET = "LET"
K_DO = "DO"
K_IF = "IF"
K_ELSE = "ELSE"
K_WHILE = "WHILE"
K_RETURN = "RETURN"
K_TRUE = "TRUE"
K_FALSE = "FALSE"
K_NULL = "NULL"
K_THIS = "THIS"
ARG_KIND = "ARG"

vm_types = {ARG_KIND: "argument", K_STATIC: "static", K_VAR: "local", K_FIELD: "this"}

class_var_dec = {K_FIELD, K_STATIC}
subroutine_dec = {K_CONSTRUCTOR, K_FUNCTION, K_METHOD}
type = {K_INT, K_CHAR, K_BOOLEAN}
statement_end = {";", "}"}
statement_types = {K_LET, K_IF, K_WHILE, K_DO, K_RETURN}
op = {'+': "add", '-': "sub", '*': "call Math.multiply 2", '/': "call Math.divide 2",
      '&': "and", '|': "or", '<': "gt", '>': "lt", '=': "eq"}
unary_op = {'-', '~'}
keyword_constant = {'TRUE', 'FALSE', 'NULL', 'THIS'}
static_field = {'STATIC', 'FIELD'}
func = {'CONSTRUCTOR', 'FUNCTION', 'METHOD'}
keyWords = \
    {'boolean': 'BOOLEAN',
     'char': 'CHAR',
     'class': 'CLASS',
     'constructor': 'CONSTRUCTOR',
     'do': 'DO',
     'else': 'ELSE',
     'false': 'FALSE',
     'field': 'FIELD',
     'function': 'FUNCTION',
     'if': 'IF',
     'int': 'INT',
     'let': 'LET',
     'method': 'METHOD',
     'null': 'NULL',
     'return': 'RETURN',
     'static': 'STATIC',
     'this': 'THIS',
     'true': 'TRUE',
     'var': 'VAR',
     'void': 'VOID',
     'while': 'WHILE'}

symbols = \
    {'&',
     '(',
     ')',
     '*',
     '+',
     ',',
     '-',
     '.',
     '/',
     ';',
     '<',
     '=',
     '>',
     '[',
     ']',
     '{',
     '|',
     '}',
     '~'}

keyword_switch = \
    {'BOOLEAN': 'boolean',
     'CHAR': 'char',
     'CLASS': 'class',
     'CONSTRUCTOR': 'constructor',
     'DO': 'do',
     'ELSE': 'else',
     'FALSE': 'false',
     'FIELD': 'field',
     'FUNCTION': 'function',
     'IF': 'if',
     'INT': 'int',
     'LET': 'let',
     'METHOD': 'method',
     'NULL': 'null',
     'RETURN': 'return',
     'STATIC': 'static',
     'THIS': 'this',
     'TRUE': 'true',
     'VAR': 'var',
     'VOID': 'void',
     'WHILE': 'while'}

symbol_switch = \
    {'&': '&amp;',
     '(': '(',
     ')': ')',
     '*': '*',
     '+': '+',
     ',': ',',
     '-': '-',
     '.': '.',
     '/': '/',
     '\"': '',
     ';': ';',
     '<': '&lt;',
     '=': '=',
     '>': '&gt;',
     '[': '[',
     ']': ']',
     '{': '{',
     '|': '|',
     '}': '}',
     '~': '~'}

quote_switch = {'\"': '&quot;'}
