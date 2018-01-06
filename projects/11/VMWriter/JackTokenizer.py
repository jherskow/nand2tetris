##########################################################################
# FILE : VMWriter.py
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
        self.tokens_num = []  # number of tokens in every line, the number of the tokens in line i is in cell i.
        self.current_token = ""
        self.tokens = []  # list of all the tokens in the file
        self.counter = 0  # number the current token from all the tokens in the file or the list

        # remove multi line comments
        file_string = input_file.read()
        file_string = self.remove_multi_comments(file_string)
        self.read_line(file_string)
        # print(self.tokens)

    def remove_multi_comments(self, string):
        """ removes ONLY /* */ comments from an entire file string"""

        char_list = list(string)
        in_comment = False
        new_string = ""
        in_string = False
        i = 0
        while i < len(char_list):
            if in_comment == False and char_list[i] == "\"" and in_string == False:
                new_string += char_list[i]
                in_string = True
                i += 1
                continue
            elif in_string == True:
                new_string += char_list[i]
                if char_list[i] == "\"":
                    in_string = False
                i += 1
                continue
            if in_string == False:
                if char_list[i] == "\n":  # keep newliens for line num
                    new_string += char_list[i]
                    i += 1
                    continue
                elif char_list[i] == "/" and i + 1 < len(char_list) and char_list[i + 1] == "*":
                    i += 2
                    in_comment = True
                elif char_list[i] == "*" and i + 1 < len(char_list) and char_list[i + 1] == "/":
                    i += 2
                    in_comment = False
                else:
                    if not in_comment:
                        new_string += char_list[i]
                    i += 1

        return new_string

    def get_tokens(self, line):
        """"""
        temp = line.split()  # split by space
        tokens = []
        string_word = ""
        for word in temp:
            new_word = ""
            for l in word:
                if "\"" == l and string_word == "":
                    string_word += l
                    new_word += l
                elif "\"" == l and string_word != "":
                    string_word += " " + new_word + l
                    tokens.append(string_word)
                    string_word = ""
                    new_word = ""
                elif string_word != "":
                    new_word += l
                elif l in JackTokenizer.symbols:  # if the word have a symbol
                    if new_word != "":  # first append all the words before the symbol
                        tokens.append(new_word)
                        new_word = ""
                    tokens.append(l)
                else:
                    new_word += l
            if string_word != "" and new_word != "":
                if "\"" not in new_word:
                    string_word += " " + new_word
                else:
                    string_word = new_word

            elif new_word != "":
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
        # if self.counter+1 ==len(self.tokens):
        #     self.read_line()
        if self.has_more_tokens():
            self.current_token = self.tokens[self.counter]
            self.counter += 1

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
        a = self.current_token.strip("\"")
        return a

    def go_back(self):
        self.counter -= 2
        self.current_token = self.tokens[self.counter]
        self.counter += 1

    def get_cur_line(self):  # todo
        sum = 0
        for i in self.tokens_num:
            sum += i
            if self.counter <= sum and self.counter > sum - i:
                return i

    def remove_line_comment(self, line):
        """ removes single line comments from a line"""
        is_string = False
        in_comment = False
        new_line = ""
        i = 0
        while i < len(line):
            if is_string == False and line[i] == "/" and line[i + 1] == "/":
                i += 2
                break
            elif "\"" == line[i] and in_comment == False:
                new_line += line[i]
                is_string = True
                i += 1
            else:
                new_line += line[i]
                i += 1
        return new_line

    def read_line(self, lines):
        split_lines = lines.split("\n")
        for line in split_lines:
            nextLine = self.remove_line_comment(line)
            tokens = []
            if (nextLine):
                tokens = self.get_tokens(nextLine)
                self.tokens += tokens
            self.tokens_num.append(len(tokens))
