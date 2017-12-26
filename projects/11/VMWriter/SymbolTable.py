##########################################################################
# FILE : SymbolTable.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex11 2017-2018
# DESCRIPTION:
##########################################################################




class SymbolTable:
    """
    Provides a symbol table abstraction. The symbol table associates the
    identifier names found in the program with identifier properties needed for com-
    pilation: type, kind, and running index. The symbol table for Jack programs has
    two nested scopes (class/subroutine).
    """

    def __init__(self):
        """
        Creates a new empty symbol table.
        """


    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e., resets the subroutine’s symbol table).
        """


    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
        """

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current scope.
        """

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns NONE .
        """

    def type_of(self, name):
        """Returns the type of the named identifier in the current scope."""


    def index_of(self,name):
        """Returns the index assigned to the named identifier."""