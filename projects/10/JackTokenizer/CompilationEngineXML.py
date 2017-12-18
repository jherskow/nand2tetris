##########################################################################
# FILE : CompilationEngineXML.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex10 2017-2018
# DESCRIPTION:
##########################################################################

class CompilationEngineXML:
    """
    Effects the actual compilation output.
    Gets its input from a JackTokenizer
    and emits its parsed structure into an output file/stream.

    The output is generated by a series of compilexxx() routines,
    one for every syntactic element xxx of the Jack grammar.

    The contract between these routines is
    that each compilexxx() routine should
        read the syntactic construct xxx from the input,
        advance() the tokenizer exactly beyond xxx ,
        and output the parsing of xxx .

    Thus, compilexxx() may only be called
    if indeed xxx is the next syntactic element of the input.
    """

    def CompilationEngineVM(self, input_file, output_file):
        """
        Creates a new compilation
        engine with the given input and
        output. The next routine called
        must be compileClass() .
        """

    def compile_class(self):
        """
        Compiles a complete class.
        """


    def compile_class_var_dec(self):
        """
        Compiles a static declaration or a field declaration.
        """

    def compile_subroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """

    def compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list,
        not including the enclosing ‘‘ () ’’.
        """

    def compile_var_dec(self):
        """
        Compiles a var declaration.
        """

    def compile_statements(self):
        """
        Compiles a sequence of statements,
        not including the enclosing ‘‘{}’’.
        """

    def compile_do(self):
        """
        Compiles a do statement.
        """

    def compile_let(self):
        """
        Compiles a let statement.
        """

    def compile_while(self):
        """
        Compiles a while statement.
        """

    def compile_return(self):
        """
        Compiles a return statement.
        """

    def compile_if(self):
        """
        Compiles a if statement,
        possibly with a trailing else clause.
        """

    def compile_expression(self):
        """
        Compiles a expression.
        """


    def compile_term(self):
        """
        Compiles a term.

        This routine is faced with a slight difficulty
        when trying to decide between some of the alternative parsing rules.

        Specifically, if the current token is an identifier,
        the routine must distinguish between
         a variable,
         an array entry,
         and a subroutine call.

        A single look- ahead token,
        which may be one of ‘‘[’’, ‘‘(’’, or ‘‘.’’
        suffices to distinguish between the three possibilities.

        Any other token is not part of this term
        and should not be advanced over.
        """


    def compile_expression_list(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """
