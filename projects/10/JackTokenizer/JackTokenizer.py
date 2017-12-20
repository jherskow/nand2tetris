##########################################################################
# FILE : JackTokenizer.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex10 2017-2018
# DESCRIPTION:
##########################################################################
import re


class JackTokenizer:
    """
    Removes all comments and white space from the input stream
    and breaks it into Jack-language tokens,
    as specified by the Jack grammar.
    """

    keyWords = {"class": "CLASS", "method": "METHOD", "function": "FUNCTION", "constructor": "CONSTRUCTOR",
                "int": "INT",
                "boolean": "BOOLEAN", "char": "CHAR", "void": "VOID", "var": "VAR", "static": "STATIC",
                "field": "FIELD",
                "let": "LET", "do": "DO", "if": "IF", "else": "ELSE", "while": "WHILE", "return": "RETURN",
                "true": "TRUE",
                "false": "FALSE", "null": "NULL", "this": "THIS"}
    symbols = {"(", ")", "{", "}", "[", "]", ",", ";", "=", ".", "+", "-", "*", "/", "&", "|", "~", "<", ">"}

    def __init__(self, input_file):
        """Opens the input file/stream and gets ready to tokenize it."""
        self.file = input_file
        self.lines = {}
        self.current_token = ""
        self.tokens = [] #list of all the tokens in the file
        self.counter = 0 #number the current token from all the tokens in the file or the list
        self.line_num = 0 #line number of the current token

    def remove_comments(self, line):
        """ removes comments from a line"""
        line = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", line)
        # remove all occurance streamed comments (/*COMMENT */) from string
        line = re.sub(re.compile("//.*?\n"), "\n", line)
        line = re.sub(re.compile("/\*\*.*?\*/", re.DOTALL), "", line)
        return line

    def get_tokens(self, line):
        """"""
        temp = line.split()  # split by space
        print(temp)
        tokens = []
        for word in temp:
            new_word = ""
            for l in word:
                if l in JackTokenizer.symbols:  # if the word have a symbol
                    if new_word != "":  # first append all the words before the symbol
                        tokens.append(new_word)
                        new_word = ""
                    tokens.append(l)
                else:
                    new_word += l
            if new_word != "":
                tokens.append(new_word)

        return tokens

    def has_more_tokens(self):
        """Do we have more tokens in the input?"""
        return bool(len(self.tokens) > self.counter + 1)

    def advance(self):
        """
            Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token.
        """
        if (self.has_more_tokens()):
            self.counter += 1
            self.current_token = self.tokens[self.counter]

    def token_type(self):
        """Returns the type of the current token."""

        """
        return one of
        KEYWORD, SYMBOL,
        IDENTIFIER, INT_CONST,
        STRING_CONST  
        """
        if self.keyWord_type():
            return "KEYWORD"
        elif self.symbol_type():
            return "SYMBOL"
        elif self.str_const_type():
            return "STRING_CONST"
        elif self.int_const_type():
            return "INT_CONST"
        elif self.identifier_type():
            return "IDENTIFIER"
        else:
            return None

    def keyWord_type(self):
        """return true if the current token type is keyword """
        return bool(self.current_token in JackTokenizer.keyWords)

    def symbol_type(self):
        """return true if the current token type is symbol """
        return bool(self.current_token in JackTokenizer.symbols)

    def str_const_type(self):
        """return true if the current token type is str const """
        return bool(re.fullmatch("\".*?\"", self.current_token))  # "...."

    def int_const_type(self):
        """return true if the current token type is int const"""
        return bool(re.fullmatch("([0-9])*", self.current_token))

    def identifier_type(self):
        """return true if the current token type is identifier"""
        return bool(re.fullmatch("(_|[a-z]|[A-Z])([a-z]?[A-Z]?[0-9]?_?)*", self.current_token))

    def key_word(self):
        """
        Returns the keyword which is the current token.
        Should be called only when tokenType() is KEYWORD .
        """

        """
        return one of
        CLASS, METHOD, FUNCTION,
        CONSTRUCTOR, INT,
        BOOLEAN, CHAR, VOID,
        VAR, STATIC, FIELD, LET,
        DO, IF, ELSE, WHILE,
        RETURN, TRUE, FALSE,
        NULL, THIS
        """
        return JackTokenizer.keyWords[self.current_token]

    def symbol(self):
        """
        Returns the character which is the
        current token. Should be called only
        when tokenType() is SYMBOL .
        :return: char
        """
        return self.current_token

    def identifier(self):
        """
        Returns the identifier which is the
        current token. Should be called only
        when tokenType() is IDENTIFIER .
        :return: String
        """
        return self.current_token

    def int_val(self):
        """
        Returns the integer value of the
        current token. Should be called only
        when tokenType() is INT_CONST .
        :return: Int
        """
        return int(self.current_token)

    def string_val(self):
        """
        Returns the string value of the current
        token, without the double quotes.
        Should be called only when
        tokenType() is STRING_CONST .
        :return: String
        """
        return str(self.current_token)

    def read_line(self):
        nextLine = self.file.readline()
        while nextLine:
            nextLine = self.remove_comments(nextLine)
            if (nextLine):
                self.lines[nextLine] = self.counter
                tokens = self.get_tokens(nextLine)
                self.tokens += tokens
            self.line_counter += 1
            nextLine = self.file.readline()


def main():
    s = "let sum = (numerator * other.getDenominator()) +(other.getNumerator() * denominator());"
    c = JackTokenizer("test").get_tokens(s)
    print(c)
    z = "\"465 j7\""
    print(re.fullmatch("\".*?\"", z))
    # print(re.match("([a-z]|[A-Z])",z))
    # if re.match("[0-9]*",z)!=None and re.match("([a-z]|[A-Z])",z) == None :
    #     print(111)
    a = s.split()
    x = s.split("[A-Z][a-z][0-9]")
    # print(a)
    # print(x)

if __name__ == '__main__':
    main()
