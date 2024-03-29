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

# todo - check array retrival[??]
# todo - string genertion - ???

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
        # make a new symbol table for the new class
        self.symbol_table = SymbolTable.SymbolTable()
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

        self.advance()

        # {
        self.compile_symbol_check("{", "Class must begin with {")
        self.compile_class_body()

    def compile_class_var_dec(self):
        """
        Compiles a static declaration or a field declaration.
        """

        # ( 'static' | 'field' ) type varName ( ',' varName)* ';'

        # static | field  (this is the kind)
        kind = self.key_word()
        self.advance()

        # type or class type
        if self.type() == d.KEYWORD:
            var_type = self.key_word()
        else:
            var_type = self.identifier()
        self.advance()

        # name - single varname
        name = self.identifier()
        self.advance()

        # declare in sym table by kind, name,  and and type
        self.declare_variable(name, var_type, kind)

        # possible additional ',' varname  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            # skip the ','
            self.advance()

            # another varname
            name = self.identifier()
            self.advance()

            # declare under same kind and type
            self.declare_variable(name, var_type, kind)

        # ;
        self.compile_symbol_check(";", "expected closing \";\" for declaration")

    def compile_subroutine(self):
        """
        Compiles a complete method, function, or constructor declaration.
        """

        self.symbol_table.start_subroutine()

        # ( 'constructor' | 'function' | 'method' )
        # ( 'void' | type) subroutineName '(' parameterList ')'
        # subroutineBody

        # 'constructor' | 'function' | 'method'
        subroutine_type = self.key_word()

        # cases:     'constructor' | 'function' | 'method'
        is_constructor = False
        is_method = False
        if subroutine_type == d.K_CONSTRUCTOR:
            is_constructor = True
        elif subroutine_type == d.K_METHOD:
            # declare this as the first arg
            self.declare_variable("this", self.class_name, SymbolTable.ARG_KIND)
            is_method = True
        self.advance()

        # 'void' | type
        self.advance()

        # subroutineName
        # save name as (classname.subroutinename), to be used later when writing the call
        name = self.identifier()

        self.advance()
        if self.type() == d.SYMBOL and self.symbol() == ".":
            self.advance()
            name= name +"."+self.identifier()
        else:
            name = self.class_name+"."+name
        # (
        self.compile_symbol_check("(", "expected opening \"(\" for parameterList ")

        # parameterList
        self.compile_parameter_list()

        # )
        self.compile_symbol_check(")", "expected closing \")\" for parameterList  ")

        # subroutineBody
        self.compile_subroutine_body(name, is_constructor, is_method)

    def compile_parameter_list(self):
        """
        compiles a (possibly empty) parameter list,
        not including the enclosing ()
        :return:
        """

        # ( (type varName) ( ',' type varName)*)?

        # if empty - ?
        if self.type() == d.SYMBOL and self.symbol() == ")":
            return None

        # otherwise first (type varname) must exist

        # single type or class type
        if self.type() == d.KEYWORD:
            var_type = self.key_word()
        else:
            var_type = self.identifier()
        self.advance()

        # var name
        name = self.identifier()
        self.advance()

        # declare
        self.declare_variable(name, var_type, SymbolTable.ARG_KIND)


        # possible additional type varname  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            self.advance()

            # type or class type
            if self.type() == d.KEYWORD:
                var_type = self.key_word()
            else:
                var_type = self.identifier()
            self.advance()

            # var name
            name = self.identifier()
            self.advance()

            # declare
            self.declare_variable(name, var_type, SymbolTable.ARG_KIND)


    def compile_var_dec(self):
        """
        Compiles a var declaration.
        """

        num_vars = 0
        # 'var' type varName ( ',' varName)* ';'

        # var
        if self.type() != d.KEYWORD and self.key_word() != d.K_VAR:
            raise CompilerError(self, "expected \"var\" in variable declaration")
        self.advance()

        # type or class type
        if self.type() == d.KEYWORD:
            var_type = self.key_word()
        else:
            var_type = self.identifier()
        self.advance()

        # var name
        name = self.identifier()
        self.advance()

        # declare
        self.declare_variable(name, var_type, SymbolTable.VAR_KIND)
        num_vars += 1

        # possible additional "," varname  's
        while self.type() == d.SYMBOL and self.symbol() == ",":
            # skip the ","
            self.advance()

            # var name
            name = self.identifier()
            self.advance()

            # declare
            self.declare_variable(name, var_type, SymbolTable.VAR_KIND)
            num_vars += 1

        # ';'
        self.compile_symbol_check(";", "expected ; at end of variable declaration")

        return num_vars

    def compile_statements(self):
        """
        Compiles a sequence of statements,
        not including the enclosing {}.
        """
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

        # varname
        var_name = self.identifier()
        self.advance()

        # possible [ expression ] for array index   todo [] fix
        if self.type() == d.SYMBOL and self.symbol() == "[":

            self.write_push(var_name)
            self.advance()
            self.compile_expression()
            self.compile_symbol_check("]", "expected to match [")
            #=
            self.compile_symbol_check("=", "expected in assignment")
            #expression
            self.compile_expression()

            # save value of expression
            self.write("pop temp 1\n")

            # add varname and [] exp
            self.write("add\n")

            # make the that segment point to (varname + [] exp) location
            self.write("pop pointer 1\n")

            # retrive value of expression
            self.write("push temp 1\n")

            # place value of expression at (varname + [] exp) location
            self.write("pop that 0\n")

        # no array index
        else:
            # =
            self.compile_symbol_check("=", "expected in assignment")

            # expression
            #   then do all the stuff on the right
            self.compile_expression()

            self.write_pop(var_name)




        # ;
        self.compile_symbol_check(";", "expected ; at end of assignment")

    def compile_do(self):
        """
        Compiles a do statement.
        """
        # 'do' subroutineCall ';'

        # do
        self.advance()

        # subroutineCall
        self.compile_subroutine_call()

        # ignore return value (which always exists)
        self.write("pop temp 0\n")  #todo check

        # ;
        self.compile_symbol_check(";", "expected ; after subroutine call")

    def compile_while(self):
        """
        Compiles a while statement.
        """

        # 'while' '(' expression ')' '{' statements '}'


        # while
        loop_num = str(self.loop_count)
        self.loop_count +=1
        self.write_label("whileStart" + loop_num)
        self.advance()

        # '(' expression ')
        self.compile_symbol_check("(", "expected ( in (expression) for while")
        self.compile_expression()
        self.compile_symbol_check(")", "expected ) in (expression) for while")

        # if not expresssion - go to end
        self.write_arithmetic("not")
        self.write_if_goto("whileEnd" + loop_num)

        #otherwise, statements


        # '{' statements '}'
        self.compile_symbol_check("{", "expected { in {statements} for while")
        self.compile_statements()
        self.compile_symbol_check("}", "expected } in {statements} for while")

        # go to while, and check again
        self.write_goto("whileStart" + loop_num)

        # mark end
        self.write_label("whileEnd" + loop_num)

    def compile_return(self):
        """
        Compiles a return statement.
        """

        # 'return' expression? ';'

        # return
        self.advance()

        # expression?   - must be non-void function.
        if self.type() != d.SYMBOL or self.symbol() != ";":
            self.compile_expression()
        # return; - must be void function.
        elif self.type() == d.SYMBOL and self.symbol() == ";":
            self.write("push constant 0\n")

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
        if_num = self.if_count
        self.if_count += 1
        self.write_if_goto("ifElse" + str(if_num))




        # '{' statements '}'
        self.compile_symbol_check("{", "expected { in {statements} for if")
        self.compile_statements()
        self.compile_symbol_check("}", "expected } in {statements} for if")
        self.write_goto("ifEnd" + str(if_num))

        self.write_label("ifElse" + str(if_num))
        # else
        if self.type() == d.KEYWORD and self.key_word() == d.K_ELSE:
            # else
            self.advance()

            # '{' statements '}'
            self.compile_symbol_check("{", "expected { in {statements} for else")
            self.compile_statements()
            self.compile_symbol_check("}", "expected } in {statements} for else")

        self.write_label("ifEnd" + str(if_num))

    def compile_expression(self):
        """
        Compiles a expression.
        """

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

                if self.symbol() == "[":    # todo [] fix
                    # varname[expression]
                    self.retreat()

                    # varname
                    self.compile_var_name()

                    # [
                    self.compile_symbol_check("[", "[ expected for array index")

                    #  expression
                    self.compile_expression()

                    # [
                    self.compile_symbol_check("]", "] expected for array index")

                    #push *(varname+exp)
                    self.write_arithmetic("add")
                    # make that point to (varname+exp)
                    self.write("pop pointer 1\n")
                    # push that[0] to stack
                    self.write("push that 0\n")



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
            unary_op= self.symbol()
            self.advance()
            self.compile_term()
            self.write_arithmetic(d.unary_op[unary_op])

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
        args_num += 1

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

        # while next tok matches classVarDec, compile all class var decs
        while self.type() == d.KEYWORD and self.key_word() in d.static_field:
            #  (static or field)
            self.compile_class_var_dec()

        # while next toks match subroutineDec, compile subroutineDec
        while self.type() == d.KEYWORD and self.key_word() in d.func:
            self.compile_subroutine()

        # ensure next token is }
        self.compile_symbol_check("}", "} expected at end of Class.")

    def compile_var_name(self):
        """
        write a variable name
        """
        # push name index
        self.write_push(self.identifier())
        self.advance()

    def compile_symbol_check(self, symbol, message):
        if self.type() != d.SYMBOL or self.symbol() != symbol:
            print()
            raise CompilerError(self, message)
        self.advance()

    def compile_subroutine_call(self):  # todo check
        """
        Compiles a call to a subroutine
        """
        # subroutineName '(' expressionList ')' | (className |varName) '.' subroutineName '(' expressionList ')'
        # possibilities are
        # func(list)
        # class.func(list)
        # var.func(list)

        # look forward
        self.advance()

        args_num = 0

        # if no "." =this is just  foo() - we want to call foo in current class
        if self.type() == d.SYMBOL and self.symbol() == "(":
            # subroutineName '(' expressionList ')'
            self.retreat()

            # subroutineName = class.foo
            subroutine_name = self.class_name + "." + self.identifier()
            self.advance()

            # (
            self.compile_symbol_check("(", "expected ( for function arguments")

            # expressionList
            args_num += self.compile_expression_list()

            # )
            self.compile_symbol_check(")", "expected ) for function arguments")

            #call subroutine_name args_num
            self.write("push pointer 0\n")
            self.write_call(subroutine_name,args_num+1)


        #  if "." - then this is class.foo or object.foo
        elif self.type() == d.SYMBOL and self.symbol() == ".":
            # (className |varName) '.' subroutineName '(' expressionList ')'
            self.retreat()

            # (className |varName)
            class_or_var_name = self.identifier()
            self.advance()

            # '.'
            self.compile_symbol_check(".", "expected . for class.method")

            # subroutineName  (method / func name)
            subroutine_name = self.identifier()

            # object.method
            if (class_or_var_name in self.symbol_table.subroutine_identifiers)\
                    or (class_or_var_name in self.symbol_table.class_identifiers):

                object_name = class_or_var_name

                # the type is in our vars
                objects_class_name = self.symbol_table.type_of(object_name)

                # push the variable (which is the object's address)
                self.write_push(object_name)

                # call type.method with 1 extra arg
                subroutine_name = objects_class_name + "." + subroutine_name
                args_num += 1

            # OtherClass.func
            else: # type_or_none_if_class is None

                # call OtherClass.func
                func_class_name = class_or_var_name
                subroutine_name = func_class_name + "." + subroutine_name

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

    def compile_subroutine_body(self, name, is_constructor, is_method):
        """
        Complies a subroutine body
        """
        # '{' varDec* statements '}'

        # '{'
        self.compile_symbol_check("{", "Expected { to open method body")

        #  varDec*
        num_locals = 0
        while self.type() == d.KEYWORD and self.key_word() == d.K_VAR:
            num_locals += self.compile_var_dec()


        # write the function declaration
        self.write_function(name, num_locals)

        # if constructor, write alloc
        if is_constructor:
            self.write("push constant "+str(self.symbol_table.field_counter)+"\n")
            #  call Memory.alloc (# fields) // stack now has pointer for memory
            self.write("call Memory.alloc 1\n")

            #  set this segment to point to base adress
            self.write("pop pointer 0\n")

        # elif method, point THIS segment
        elif is_method:
            # push this adress to stack
            self.write("push argument 0\n")
            # point THIS segment
            self.write("pop pointer 0\n")

        # statements
        self.compile_statements()

        # '}'
        self.compile_symbol_check("}", "Expected } to close method body")

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
        length = len(self.string_val())
        self.write("push constant " + str(length) + "\n")
        self.write("call String.new 1\n")
        string_const = self.string_val()
        string_const = self.replace_escaped_chars(string_const)
        for char in string_const:
            self.write("push constant " + str(ord(char)) + "\n")  # todo see if correct - unicode conversion
            self.write("call String.appendChar 2\n")              # see if correct - way to create string
        self.advance()

    def compile_keyword_const(self):
        keyword = self.key_word()
        if keyword not in d.keyword_constant:
            raise CompilerError(self, "bad keyword constant")
        # true - need (-1) so -  push 1 and call neg
        if keyword == "TRUE":
            self.write("push constant 0\n")
            self.write("not\n")
        # false / null -   push constant 0
        elif keyword in {"FALSE", "NULL"}:
            self.write("push constant 0\n")
        elif keyword == "THIS":
            self.write("push pointer 0\n")
        self.advance()

# VM HELPER FUNCTIONS=========================
    def make_symbol_table(self):
        """make a new symbol table"""
        self.symbol_table = SymbolTable.SymbolTable()

    def declare_variable(self, name, var_type, kind):
        """declare a variable in the symbol table"""
        self.symbol_table.define(name, var_type, kind)

    # def get_kind(self):
    #     """ returns kind of the identifier (VAR, ARD, FIELD, STATIC)"""
    #     kind = self.key_word()
    #     if kind == "var":
    #         return SymbolTable.VAR_KIND
    #     elif kind == "static":
    #         return SymbolTable.STATIC_KIND
    #     elif kind == "field":
    #         return SymbolTable.STATIC_KIND
    #     else:
    #         return SymbolTable.ARG_KIND

    def write_push(self, name):
        self.vm_writer.write_push(d.vm_types[self.symbol_table.kind_of(name)],
                                  self.symbol_table.index_of(name))

    def write_pop(self, name):
        self.vm_writer.write_pop(d.vm_types[self.symbol_table.kind_of(name)],
                                 self.symbol_table.index_of(name))

    def write_function(self, name, n_locals):
        self.vm_writer.write_function(name, n_locals)

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

    def write_if_goto(self, label):
        self.vm_writer.write_if_goto(label)

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

    def replace_escaped_chars(self,string):
        replace = {"\t":"\\t","\n":"\\n","\r":"\\r","\b":"\\b"}
        for escaped in replace.keys():
            string = string.replace(escaped, replace[escaped])
        return string

class CompilerError(SyntaxError):
    def __init__(self, engine, message=""):
        num = engine.token.counter
        s = 10
        max = min([num+s, len(engine.token.tokens)])
        toklist = [engine.token.tokens[i] for i in range(num-s,max)]
        words = ""
        for word in toklist:
            words += word + " "
        self.msg = "error in file\n" + engine.output_file.name + \
                   "\nerror in line " + str(engine.line_num()) + "\n" + \
                   message + "\n" + "line:  " + words
