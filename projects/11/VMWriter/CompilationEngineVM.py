##########################################################################
# FILE : CompilationEngineXML.py
# WRITER : Josuha Herskowitz , jherskow , 321658379
# WRITER : Aya Jbara , ayaj , 209048156
# EXERCISE : nand2tetris ex10 2017-2018
# DESCRIPTION:
##########################################################################
import char_dict as d
import SymbolTable
import VMWriter


class CompilationEngineVM:
    """
    Effects the actual compilation output.
    Gets its input from a VMWriter
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

    def __init__(self, tokenizer, output_file):
        """
        Creates a new compilation
        engine with the given input and
        output. The next routine called
        must be compileClass() .
        """
        self.output_file = output_file
        self.token = tokenizer
        self.vm_writer = VMWriter.VMWriter(output_file)
        self.symbol_table = None
        self.class_name = ""
        self.if_count = 0
        self.loop_count = 0

        # get first token
        self.advance()

        if self.type() != d.KEYWORD or self.key_word() != d.K_CLASS:
            raise CompilerError(self, "File must begin with \"class\"")

        self.compile_class()


    def compile_class(self):
        """
        Compiles a complete class.
        """

        # class
        self.advance()

        # name
        if self.type() != d.IDENTIFIER:
            raise CompilerError(self, "Class must begin with class name")
        self.class_name = self.identifier()
        # make a new symbol table for the new class
        self.symbol_table = SymbolTable.SymbolTable()
        self.advance()

        # {
        self.compile_symbol_check("{", "Class must begin with {")
        self.compile_class_body()

    def compile_class_var_dec(self):
        """
        Compiles a static declaration or a field declaration.
        """

        # ( 'static' | 'field' ) type varName ( ',' varName)* ';'

        # declare field 'this'
        self.declare_variable("this", self.class_name, SymbolTable.FIELD_KIND)

        # static | field  (this is the kind)
        kind = self.get_kind()
        self.advance()

        # type  - int/double/ClassName
        type = self.identifier()
        self.advance()

        # name - single varname
        name = self.identifier()
        self.advance()

        # declare in sym table by kind, name,  and and type
        self.declare_variable(name, type, kind)

        # possible additional ',' varname  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            # skip the ','
            self.advance()

            # another varname
            name = self.identifier()
            self.advance()

            # declare under same kind and type
            self.declare_variable(name, type, kind)

        # ;
        self.compile_symbol_check(";", "expected closing \";\" for declaration")

    def compile_subroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """

        # ( 'constructor' | 'function' | 'method' )
        # ( 'void' | type) subroutineName '(' parameterList ')'
        # subroutineBody

        # 'constructor' | 'function' | 'method'
        subroutine_type = self.key_word()

        # cases:     'constructor' | 'function' | 'method'
        if subroutine_type == d.K_CONSTRUCTOR:
            #  call Memory.alloc (# fields) // stack now has pointer for memory
            self.vm_writer.write("call Memory.alloc " + str(self.symbol_table.field_counter) + ")\n")
            # t  pop pointer 0           // make object's 'this' field equal this pointer
            self.vm_writer.write(
                "pop pointer 0\n")  # todo check correct location!!!! - (we want the 'this' field to contain the value returned by malloc)
        elif subroutine_type == d.K_METHOD:
            # declare this as the first method, and make i
            self.declare_variable("this", self.class_name, SymbolTable.ARG_KIND)
        self.advance()

        # 'void' | type # todo do we care?
        self.advance()

        # subroutineName
        # save name as (classname.subroutinename), to be used later wehn writing the call
        name = self.class_name + "." + self.identifier()

        self.advance()

        # (
        self.compile_symbol_check("(", "expected opening \"(\" for parameterList ")

        # parameterList
        self.compile_parameter_list()

        # )
        self.compile_symbol_check(")", "expected closing \")\" for parameterList  ")

        # subroutineBody
        self.compile_subroutine_body(name)

        self.symbol_table.start_subroutine()

    def compile_parameter_list(self):
        """
        compiles a (possibly empty) parameter list,
        not including the enclosing ()
        :return:
        """
        n_locals = 0
        # ( (type varName) ( ',' type varName)*)?

        # if empty - ?
        if self.type() == d.SYMBOL and self.symbol() == ")":
            return n_locals

        # otherwise first (type varname) must exist

        # single type varName
        # type
        type = self.identifier()  # todo OR IDENTIFIER
        self.advance()

        # var name
        name = self.identifier()
        self.advance()

        # declare
        self.declare_variable(name, type, SymbolTable.ARG_KIND)  # todo check ARG is correct

        # push kind index
        self.write_push(name)
        n_locals += 1

        # possible additional type varname  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            self.advance()

            # type
            type = self.key_word()  # todo OR IDENTIFIER
            self.advance()

            # var name
            name = self.identifier()
            self.advance()

            # declare
            self.declare_variable(name, type, SymbolTable.ARG_KIND)  # todo check ARG is correct

            # push kind index
            self.write_push(name)
            n_locals += 1

        return n_locals

    def compile_var_dec(self):
        """
        Compiles a var declaration.
        """

        # 'var' type varName ( ',' varName)* ';'

        # var
        if self.type() != d.KEYWORD and self.key_word() != d.K_VAR:
            raise CompilerError(self, "expected \"var\" in variable declaration")
        self.advance()

        # single type varName

        # type
        type = self.identifier()  # todo OR IDENTIFIER
        self.advance()

        # var name
        name = self.identifier()
        self.advance()

        # declare
        self.declare_variable(name, type, SymbolTable.VAR_KIND)  # todo check ARG is correct
        self.write_push(name)

        # possible additional "," varname  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            # skip the ","
            self.advance()

            # type
            # type = self.key_word()  # todo OR IDENTIFIER or just token?// token
            # self.advance()

            # var name
            name = self.identifier()
            self.advance()

            # declare
            self.declare_variable(name, type, SymbolTable.VAR_KIND)  # todo check ARG is correct
            self.write_push(name)

        # ';'
        self.compile_symbol_check(";", "expected ; at end of variable declaration")

    def compile_statements(self):
        """
        Compiles a sequence of statements,
        not including the enclosing {}.
        """
        # todo == does this need anything?
        # statement*  0 or more times

        while self.type() == d.KEYWORD and self.key_word() in d.statement_types:
            statement_type = self.key_word()

            if statement_type == d.K_LET:
                self.compile_let()
            elif statement_type == d.K_IF:
                self.compile_if()
            elif statement_type == d.K_WHILE:
                self.compile_while()
            elif statement_type == d.K_DO:
                self.compile_do()
            elif statement_type == d.K_RETURN:
                self.compile_return()

    def compile_let(self):
        """
        Compiles a let statement.
        """

        # 'let' varName ( '[' expression ']' )? '=' expression ';'

        # let
        self.advance()

        # ==todo ====  save name (and index, if there is)
        # ==todo ====  compute where var[expression] is so we can pop to it
        # varname
        var_name = self.identifier()
        self.advance()

        # possible [ expression ] for array index
        if self.type() == d.SYMBOL and self.symbol() == "[":
            self.write_push(var_name)
            self.advance()
            self.compile_expression()

            #(varname+exp)
            self.write_arithmetic("add")
            self.write("pop pointer 1\n")
            self.compile_symbol_check("]", "expected to match [")
            #=
            self.compile_symbol_check("=", "expected in assignment")
            #expression
            self.compile_expression()
            #   *(varname+exp)= exp
            self.write("pop that 0\n")

        else:
            self.write_push(var_name)
            self.write("pop pointer 0\n")
            # =
            self.compile_symbol_check("=", "expected in assignment")

            # expression
            #   then do all the stuff on the right
            self.compile_expression()

            # todo ====  finally, pop the value at top of stack (the result of the right)
            # todo ====  to VM location for name OR name[expression]
            self.write_pop(var_name)


        # ;
        self.compile_symbol_check(";", "expected ; at end of assignment")

    def compile_do(self):
        """
        Compiles a do statement.
        """
        # todo == should be ok
        # 'do' subroutineCall ';'

        # do
        self.advance()

        # subroutineCall
        self.compile_subroutine_call()

        # ;
        self.compile_symbol_check(";", "expected ; after subroutine call")

    def compile_while(self):
        """
        Compiles a while statement.
        """

        # 'while' '(' expression ')' '{' statements '}'


        # while
        self.write_label("LOOP" + str(self.loop_count))
        self.advance()

        # '(' expression ')
        self.compile_symbol_check("(", "expected ( in (expression) for while")
        self.compile_expression()
        self.compile_symbol_check(")", "expected ) in (expression) for while")

        self.write_arithmetic("not")
        self.write_if("L" + str(self.if_count))

        # '{' statements '}'
        self.compile_symbol_check("{", "expected { in {statements} for while")
        self.compile_statements()
        self.compile_symbol_check("}", "expected } in {statements} for while")
        self.write_goto("LOOP" + str(self.loop_count))
        self.write_label("L" + str(self.if_count))
        self.if_count+=1
        self.loop_count+=1

    def compile_return(self):
        """
        Compiles a return statement.
        """

        # 'return' expression? ';'

        # return
        self.advance()

        # expression?
        if not (self.type() == d.SYMBOL and self.symbol() == ";"):
            self.compile_expression()

        # ';'
        self.compile_symbol_check(";", "expected ; for return")
        self.write_return()

    def compile_if(self):
        """
        Compiles a if statement,
        possibly with a trailing else clause.
        """

        # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?

        self.advance()

        # '(' expression ')'
        self.compile_symbol_check("(", "expected ( in (expression) for if")
        self.compile_expression()
        self.compile_symbol_check(")", "expected ) in (expression) for if")
        self.write_arithmetic("not")
        self.write_if("L" + str(self.if_count))
        self.if_count+=1
        # '{' statements '}'
        self.compile_symbol_check("{", "expected { in {statements} for if")
        self.compile_statements()
        self.compile_symbol_check("}", "expected } in {statements} for if")
        # else

        if self.type() == d.KEYWORD and self.key_word() == d.K_ELSE:
            self.write_goto("L" + str(self.if_count))
            # else
            self.write_label("L" + str(self.if_count - 1))
            self.advance()

            # '{' statements '}'
            self.compile_symbol_check("{", "expected { in {statements} for else")
            self.compile_statements()
            self.compile_symbol_check("}", "expected } in {statements} for else")
            self.write_label("L" + str(self.if_count))
        else:
            self.write_label("L" + str(self.if_count - 1))
        self.if_count+=1

    def compile_expression(self):
        """
        Compiles a expression.
        """
        # todo == what does this do?
        # todo ==     ? probbly leave the final value on the stack ?

        # term (op term)*

        # term
        self.compile_term()

        # (op term)*  0 or more times
        while self.type() == d.SYMBOL and self.symbol() in d.op:
            op = self.compile_op()
            self.compile_term()
            self.write(op +"\n")



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
        which may be one of [, (, or .
        suffices to distinguish between the three possibilities.
        Any other token is not part of this term
        and should not be advanced over.
        """

        first_type = self.type()

        # 52
        if first_type == d.INT_CONST:
            self.compile_int_const()

        # "hello"
        elif first_type == d.STRING_CONST:
            self.compile_str_const()

        #true/false/this/null
        elif first_type == d.KEYWORD:
            self.compile_keyword_const()

        elif first_type == d.IDENTIFIER:
            # could be varname, varname[expression], subroutine call ( "(" )
            self.advance()
            if self.type() == d.SYMBOL:

                if self.symbol() == "[":
                    # varname[expression]
                    self.retreat()

                    # varname
                    self.compile_var_name()

                    # [
                    self.compile_symbol_check("[", "[ expected for array index")

                    #  expression
                    self.compile_expression()

                    #(varname+exp)
                    self.write_arithmetic("add")
                    self.write("pop pointer 1\n")

                    # [
                    self.compile_symbol_check("]", "] expected for array index")

                elif self.symbol() in {"(", "."}:
                    self.retreat()
                    self.compile_subroutine_call()

                else:
                    self.retreat()
                    self.write_push(self.identifier())
                    self.advance()

            else:
                self.retreat()
                self.write_push(self.identifier())
                self.advance()

        elif first_type == d.SYMBOL and self.symbol() == "(":
            # (expression)

            # (
            self.advance()

            # expression
            self.compile_expression()

            # )
            self.compile_symbol_check(")", "expression should end with ) ")

        elif first_type == d.SYMBOL and self.symbol() in d.unary_op:
            # unOp term
            self.advance()
            self.compile_term()
            self.write_arithmetic("not")

        else:
            raise CompilerError(self, "invalid term")

    def compile_expression_list(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """
        args_num = 0

        # (expression ( ',' expression)* )?
        # nothing, an expression, or many

        # empty
        if self.type() == d.SYMBOL and self.symbol() == ")":
            return args_num

        # one expression
        self.compile_expression()

        # possible additional expressions  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            self.advance()
            self.compile_expression()
            args_num += 1

        return args_num

    # sub compiler functions __________________________

    def compile_class_body(self):
        """
        Complies the body of a class
        """
        # we are now at first line in class

        # while next toks match classVarDec, compile class var dec
        while self.type() == d.KEYWORD and self.key_word() in d.static_field:
            #  static or field)
            self.compile_class_var_dec()

        # while next toks match subroutineDec, compile subroutineDec
        while self.type() == d.KEYWORD and self.key_word() in d.func:
            self.compile_subroutine()

        # ensure next token is }
        self.compile_symbol_check("}", "} expected at end of Class.")

    # def compile_type(self):
    #     """
    #     Compiles a type
    #     :return:
    #     """
    #     if self.type() == d.KEYWORD and self.key_word() in d.type:
    #         self.xml_keyword()
    #     elif self.type() == d.IDENTIFIER:
    #         self.xml_identifier()
    #     else:
    #         raise CompilerError(self, "type expected")
    #     self.advance()

    def compile_var_name(self):
        """
        write a variable name
        """
        # push name index
        self.write_push(self.identifier())
        self.advance()

    def compile_symbol_check(self, symbol, message):
        if self.type() != d.SYMBOL or self.symbol() != symbol:
            raise CompilerError(self, message)
        self.advance()

    def compile_subroutine_call(self):
        """
        """
        # subroutineName '(' expressionList ')' | (className |varName) '.' subroutineName '(' expressionList ')'
        # possibilities are
        # func(list)
        # class.func(list)
        # var.func(list)


        # TODO == todo subroutine call

        # look forward
        self.advance()
        # todo - if no "." - foo() - we want to call foo in curerent class
        # todo - if foo is method - we must also send 'this'
        args_num = 0

        if self.type() == d.SYMBOL and self.symbol() == "(":
            args_num=1
            # subroutineName '(' expressionList ')'
            self.retreat()

            # subroutineName
            subroutine_name = self.class_name + "." + self.identifier()
            self.advance()

            # (
            self.compile_symbol_check("(", "expected ( for function arguments")

            #push this
            self.write_push("this")
            # expressionList
            args_num += self.compile_expression_list()

            # )
            self.compile_symbol_check(")", "expected ) for function arguments")
            #call subroutine_name args_num
            self.write_call(subroutine_name,args_num)


        # todo - if no "." - then this is class.foo or object.foo
        elif self.type() == d.SYMBOL and self.symbol() == ".":
            # (className |varName) '.' subroutineName '(' expressionList ')'
            self.retreat()

            # (className |varName)
            class_name = self.identifier()
            self.advance()

            # '.'
            self.compile_symbol_check(".", "expected . for class.method")

            # subroutineName
            subroutine_name = class_name + "." + self.identifier()
            self.advance()

            # '('
            self.compile_symbol_check("(", "expected ( for function arguments")

            # expressionList
            args_num += self.compile_expression_list()

            # )
            self.compile_symbol_check(")", "expected ) for function arguments")
            self.write_call(subroutine_name,args_num)
        else:
            raise CompilerError(self, "Expected func(list) or class.func(list)")

    # def compile_subroutine_name(self):
    #     """
    #     Complies a subroutine name
    #     """
    #     self.xml_identifier()
    #     self.advance()

    def compile_subroutine_body(self, name):
        """
        Complies a subroutine body
        """
        # '{' varDec* statements '}'

        # '{'
        self.compile_symbol_check("{", "Expected { to open method body")

        #  varDec*
        num_locals = 0
        while self.type() == d.KEYWORD and self.key_word() == d.K_VAR:
            self.compile_var_dec()
            num_locals += 1

        # write the function declaration
        self.write_function(name, num_locals)

        # statements
        self.compile_statements()

        # '}'
        self.compile_symbol_check("}", "Expected } to close method body")

    #todo
    def compile_op(self):
        """
        compiles an operator
        """
        op = d.op[self.symbol()]
        self.advance()
        return op

    def compile_int_const(self):
        self.vm_writer.write_push("constant", self.int_val())
        self.advance()

    def compile_str_const(self):
        # complicated way to do this todo check
        length = len(self.string_val())
        self.write("push constant " + str(length) + "\n")
        self.write("call String.new 1\n")
        for char in self.string_val():
            self.write("push constant " + str(ord(char)) + "\n")  # todo see if correct
            self.write("call String.appendChar 1\n")
        self.advance()

    def compile_keyword_const(self):
        keyword = self.key_word()
        if keyword not in d.keyword_constant:
            raise CompilerError(self, "bad keyword constant")
        # true - need (-1) so -  push 1 and call neg
        if keyword == "TRUE":
            self.write("push constant 1\n")
            self.write("neg\n")
        # false / null -   push constant 0
        elif keyword in {"FALSE", "NULL"}:
            self.write("push constant 0\n")
        elif keyword == "THIS":
            self.write("push pointer 0\n")
        self.advance()

    # todo VM HELPER FUNCTIONS=========================
    def make_symbol_table(self):
        """make a new sybol table"""
        self.symbol_table = SymbolTable.SymbolTable()

    def declare_variable(self, name, type, kind):
        """make a new sybol table"""
        self.symbol_table.define(name, type, kind)

    def get_kind(self):
        """ returns kind of the identifier (VAR, ARD, FIELD, STATIC)"""
        kind = self.key_word()
        if kind == "var":
            return SymbolTable.VAR_KIND
        elif kind == "static":
            return SymbolTable.STATIC_KIND
        elif kind == "field":
            return SymbolTable.STATIC_KIND
        else:
            return SymbolTable.ARG_KIND

    # todo VM HELPER FUNCTIONS=========================
    def write_push(self, name):
        self.vm_writer.write_push(d.vm_types[self.symbol_table.kind_of(name)],
                                  self.symbol_table.index_of(name))

    def write_pop(self, name):
        self.vm_writer.write_pop(self.symbol_table.kind_of(name),
                                 self.symbol_table.index_of(name))

    def write_function(self, name, n_locals):
        method_name = self.class_name + "." + name
        self.vm_writer.write_function(method_name, n_locals)

    def write_return(self):
        self.vm_writer.write_return()

    def write_call(self, name, index):
        self.vm_writer.write_call(name, index)

    def write(self, string):  #
        """
        writes a string to output file
        """
        self.vm_writer.write(string)

    def write_arithmetic(self,command):
        """Writes a VM arithmetic command."""
        self.vm_writer.write_arithmetic(command)

    def write_if(self,label):
        self.vm_writer.write_if(label)

    def write_goto(self, label):
        self.vm_writer.write_goto(label)

    def write_label(self, label):
        self.vm_writer.write_label(label)

    # HELPER FUNCTIONS __________________________



    def advance(self):
        self.token.advance()

    def retreat(self):
        self.token.go_back()

    def line_num(self):
        return self.token.get_cur_line()

    def type(self):
        return self.token.token_type()

    def key_word(self):
        return self.token.key_word()

    def symbol(self):
        return self.token.symbol()

    def identifier(self):
        return self.token.identifier()

    def int_val(self):
        return self.token.int_val()

    def string_val(self):
        return self.token.string_val()


class CompilerError(SyntaxError):
    def __init__(self, engine, message=""):
        self.msg = "error in file\n" + engine.output_file.name + \
                   "\nerror in line " + str(engine.line_num()) + "\n" + \
                   message + "\n"
