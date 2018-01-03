##########################################################################
# FILE : SymbolTable.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex11 2017-2018
# DESCRIPTION:
##########################################################################


VAR_KIND = "VAR"
ARG_KIND = "ARG"
FIELD_KIND = "FIELD"
STATIC_KIND = "STATIC"


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
        self.static_counter = 0
        self.field_counter = 0
        self.argument_counter = 0
        self.var_counter = 0
        self.class_identifiers = {}
        self.subroutine_identifiers = {}


    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e., resets the subroutine’s symbol table).
        """
        self.argument_counter = 0
        self.var_counter = 0
        self.subroutine_identifiers = {}

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
        """

        if kind == VAR_KIND:
            self.var_counter += 1
            self.subroutine_identifiers[name] = [type, kind, self.var_counter]
        elif kind == ARG_KIND:
            self.argument_counter += 1
            self.subroutine_identifiers[name] = [type, kind, self.argument_counter]
        elif kind == STATIC_KIND:
            self.static_counter += 1
            self.class_identifiers[name] = [type, kind, self.static_counter]
        elif kind == FIELD_KIND:
            self.field_counter += 1
            self.class_identifiers[name] = [type, kind, self.field_counter]


    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current scope.
        kind = (STATIC ,FIELD , ARG ,or VAR)
        """
        if kind == STATIC_KIND:
            return self.static_counter
        elif kind == FIELD_KIND:
            return self.field_counter
        elif kind == ARG_KIND:
            return self.argument_counter
        elif kind == VAR_KIND:
            return self.var_counter
        else:
            return -1

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns NONE .
        """

        if self.class_identifiers.get(name) != None:
            return self.class_identifiers.get(name)[1]
        elif self.subroutine_identifiers.get(name) != None:
            return self.subroutine_identifiers.get(name)[1]
        else:
            return None

    def type_of(self, name):
        """Returns the type of the named identifier in the current scope."""
        if self.class_identifiers.get(name) != None:
            return self.class_identifiers.get(name)[0]
        elif self.subroutine_identifiers.get(name) != None:
            return self.subroutine_identifiers.get(name)[0]
        else:
            return None

    def index_of(self, name):
        """Returns the index assigned to the named identifier."""
        if self.class_identifiers.get(name) != None:
            return self.class_identifiers.get(name)[2]
        elif self.subroutine_identifiers.get(name) != None:
            return self.subroutine_identifiers.get(name)[2]
        else:
            return -1
