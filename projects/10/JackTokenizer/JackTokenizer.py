##########################################################################
# FILE : JackTokenizer.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex10 2017-2018
# DESCRIPTION:
##########################################################################


class JackTokenizer:
    """
    Removes all comments and white space from the input stream
    and breaks it into Jack-language tokens,
    as specified by the Jack grammar.
    """




    def JackTokenizer(self, input_file):
        """Opens the input file/stream and gets ready to tokenize it."""
        self.current_token=""
        self.tokens = []
        self.tokens = self.tokenize()

    def tokenize(self):
        """:returns a list of tokens"""
        #todo

    def has_more_tokens(self):
        """Do we have more tokens in the input?"""


    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        This method should only be called if hasMoreTokens() is true.
        Initially there is no current token.
        """

    def token_type(self):
        """Returns the type of the current token."""

        """
        return one of
        KEYWORD, SYMBOL,
        IDENTIFIER, INT_CONST,
        STRING_CONST  
        """

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

    def symbol(self):
        """
        Returns the character which is the
        current token. Should be called only
        when tokenType() is SYMBOL .
        :return: char
        """

    def identifier(self):
        """
        Returns the identifier which is the
        current token. Should be called only
        when tokenType() is IDENTIFIER .
        :return: String
        """

    def int_val(self):
        """
        Returns the integer value of the
        current token. Should be called only
        when tokenType() is INT_CONST .
        :return: Int
        """

    def string_val(self):
        """
        Returns the string value of the current
        token, without the double quotes.
        Should be called only when
        tokenType() is STRING_CONST .
        :return: String
        """

