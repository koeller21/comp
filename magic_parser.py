import token

class Parser(object):

    def __init__(self, token_head):
        self.cur_token = token_head

    def statement(self, syntax_tree):

        functionDefinitionSet = [token.MAGIC]
        identifierSet = [token.IDENTIFIER]
        semicolonSet = [token.SEMICOLON]
        ifSet = [token.IF]
        returnSet = [token.RETURN]

        if self.lookAhead(functionDefinitionSet):
            return self.function_definition(syntax_tree.insertSubtree(token.FUNCTIONDEF)) and self.statement(syntax_tree.insertSubtree(token.STATEMENT))
        elif self.lookAhead(identifierSet):
            if self.cur_token.get_next().get_next().get_token_type() == token.OPEN_PARA: # statement ist funktionsaufruf
                return self.application_statement(syntax_tree.insertSubtree(token.APPLICATION)) and self.match(semicolonSet, syntax_tree) and self.statement(syntax_tree.insertSubtree(token.STATEMENT))
            else:                                                           # statement ist variablenzuweisung
                return self.assignment_statement(syntax_tree.insertSubtree(token.ASSIGNMENT)) and self.match(semicolonSet, syntax_tree) and self.statement(syntax_tree.insertSubtree(token.STATEMENT))
        elif self.lookAhead(ifSet):
            return self.conditional(syntax_tree.insertSubtree(token.CONDITIONAL)) and self.statement(syntax_tree.insertSubtree(token.STATEMENT))
        elif self.lookAhead(returnSet):
            return self.return_statement(syntax_tree.insertSubtree(token.RETURN)) and self.match(semicolonSet, syntax_tree)
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True

    def lookAhead(self, matchSet):
        for token in matchSet:
            if self.cur_token.get_next() != None: # Wenn nicht EOF
                if token == self.cur_token.get_next().get_token_type():
                    return True
        return False

    def match(self, matchSet, syntax_tree):
        for token in matchSet:
            if self.cur_token.get_next() != None: # Wenn nicht EOF
                if token == self.cur_token.get_next().get_token_type():
                    new_node = syntax_tree.insertSubtree(token, self.cur_token.get_next().get_data())
                    self.cur_token = self.cur_token.get_next()

                    return True
        return False

    ### Grammatik-Regeln ####

    # FunctionDefinition -> magic Func-Name(parameter){ statement }
    def function_definition(self, syntax_tree):

        magicSet = [token.MAGIC]
        functionNameSet = [token.IDENTIFIER]
        openParSet = [token.OPEN_PARA]
        closedParSet = [token.CLOSED_PARA]
        openCurlySet = [token.OPEN_CURLY]
        closedCurlySet = [token.CLOSED_CURLY]

        if self.match(magicSet, syntax_tree):            # guck, ob magic richtig
            if self.match(functionNameSet, syntax_tree): # guck, ob func-name identifier
                if self.match(openParSet, syntax_tree):  # guck, ob ( richtig
                    if self.parameter(syntax_tree.insertSubtree(token.PARAMETER)):    # guck, ob parameter richtig
                        if self.match(closedParSet, syntax_tree): # guck, ob ) richtig
                            if self.match(openCurlySet, syntax_tree): # guck, ob { richtig
                                if self.statement(syntax_tree.insertSubtree(token.STATEMENT)):
                                    if self.match(closedCurlySet, syntax_tree):
                                        return True
                                    else:
                                        print("Geschwungene Klammer vergessen!")
                                        return False
                                else:
                                    print("Fehler in Funktion!")
                                    return False
                            else:
                                print("Geschwungene Klammer vergessen!")
                                return False
                        else:
                            print("Geschlossene Rundklammern vergessen!")
                            return False
                    else:
                        print("Parameter falsch!")
                        return False
                else:
                    print("Offene Rundklammern vergessen!")
                    return False
            else:
                print("Funktionsname vergessen oder falsch!")
                return False
        else:
            print("Magic keyword falsch oder vergessen!")
            return False

    #parameter -> identifier R | epsilon
    def parameter(self, syntax_tree):
        identifierSet = [token.IDENTIFIER]
        if self.lookAhead(identifierSet):
            return self.identifier(syntax_tree) and self.r(syntax_tree.insertSubtree("R"))
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True


    def identifier(self, syntax_tree):
        self.match([token.IDENTIFIER], syntax_tree)
        return True

    # R -> ',' parameter R | epsilon
    def r(self, syntax_tree):
        commaSet = [token.COMMA]
        if self.match(commaSet, syntax_tree):
            return self.parameter(syntax_tree.insertSubtree(token.PARAMETER)) and self.r(syntax_tree.insertSubtree("R"))
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True

    # AssignmentStatement -> identifier '=' Expression | identifier '=' Bool_Expression | identifier '=' var_string | identifier '=' identifier | identifier '=' applicationStatement
    def assignment_statement(self, syntax_tree):

        equalsSet = [token.EQUALS]
        varNumSet = [token.VAR_NUM]
        varStringSet = [token.VAR_STRING]
        varBoolSet = [token.VAR_BOOL, token.OPEN_PARA]
        varExpressionSet = [token.VAR_NUM, token.OPEN_PARA]
        varOperatorSet = [token.DIV, token.MUL, token.PLUS, token.MINUS]
        identifierSet = [token.IDENTIFIER]

        if self.identifier(syntax_tree):
            if self.match(equalsSet, syntax_tree):

                if self.lookAhead(varExpressionSet) or self.cur_token.get_next().get_next().get_token_type() in varOperatorSet :
                    return self.expression(syntax_tree.insertSubtree(token.EXPRESSION))
                elif self.lookAhead(varBoolSet) or self.cur_token.get_next().get_next().get_token_type() in [token.AND_LOGIC, token.OR_LOGIC]:
                    return self.boolExpression(syntax_tree.insertSubtree(token.BOOLEXPR))
                elif self.match(varStringSet, syntax_tree):
                    return True
                elif self.lookAhead(identifierSet) and self.cur_token.get_next().get_next().get_token_type() == token.OPEN_PARA:
                    return self.application_statement(syntax_tree.insertSubtree(token.APPLICATION))
                elif self.match(identifierSet, syntax_tree):
                    return True
            else:
                return False
        else:
            return False

    # expression -> term rightExpression
    def expression(self, syntax_tree):
        return self.term(syntax_tree.insertSubtree(token.TERM)) and self.rightExpression(syntax_tree.insertSubtree(token.RIGHTEXPRESSION))

    # rightExpression -> '+' term rightExpression | ‘‐' term rightExpression | ε
    def rightExpression(self, syntax_tree):
        plusMinusOpSet = [token.MINUS, token.PLUS]
        if self.match(plusMinusOpSet, syntax_tree):
            return self.term(syntax_tree.insertSubtree(token.TERM)) and self.rightExpression(syntax_tree.insertSubtree(token.RIGHTEXPRESSION))
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True

    #     term -> operator rightTerm
    def term(self, syntax_tree):
        return self.operator(syntax_tree.insertSubtree(token.OPERATOR)) and self.rightTerm(syntax_tree.insertSubtree(token.RIGHTTERM))

    #     rightTerm -> '*' operator rightTerm | ‘/' operator rightTerm |  ε
    def rightTerm(self, syntax_tree):
        compOpSet = [token.MUL, token.DIV]

        if self.match(compOpSet, syntax_tree):
            return self.operator(syntax_tree.insertSubtree(token.OPERATOR)) and self.rightTerm(syntax_tree.insertSubtree(token.RIGHTTERM))
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True

    #  operator -> '(' expression ')' | identifier | expression (num)
    def operator(self, syntax_tree):
        openParaSet = [token.OPEN_PARA]
        closedParaSet = [token.CLOSED_PARA]
        identifierSet = [token.IDENTIFIER]
        numSet = [token.VAR_NUM]

        if self.match(openParaSet, syntax_tree):
            if self.expression(syntax_tree.insertSubtree(token.EXPRESSION)):
                if self.match(closedParaSet, syntax_tree):
                    return True
                else:
                    print("Rundklammern vergessen!")
                    return False
        elif self.match(identifierSet, syntax_tree):
            return True
        elif self.match(numSet, syntax_tree):
            return True
        else:
            return False




    def conditional(self, syntax_tree):

        openParaSet = [token.OPEN_PARA]
        closedParaSet = [token.CLOSED_PARA]
        openCurlySet = [token.OPEN_CURLY]
        closedCurlySet = [token.CLOSED_CURLY]
        ifSet = [token.IF]

        if self.match(ifSet, syntax_tree):
            if self.match(openParaSet, syntax_tree):
                if self.boolExpression(syntax_tree.insertSubtree(token.BOOLEXPR)):
                    if self.match(closedParaSet, syntax_tree):
                        if self.match(openCurlySet, syntax_tree):
                            if self.statement(syntax_tree.insertSubtree(token.STATEMENT)):
                                if self.match(closedCurlySet, syntax_tree):
                                    if self.cond_else(syntax_tree.insertSubtree(token.COND_ELSE)):
                                        return True
                                    else:
                                        print("Else-Zweig falsch!")
                                        return False
                                else:
                                    print("Geschlossene Geschwungene Klammern falsch oder vergessen!")
                                    return False
                            else:
                                print("Statement im if-Body falsch!")
                                return False
                        else:
                            print("Offene Geschwungene Klammern falsch oder vergessen!")
                            return False
                    else:
                        print("Geschlossene Rundklammern vergessen oder falsch!")
                        return False
                else:
                    print("Ausdruck im if-Kopf falsch!")
                    return False
            else:
                print("Offene Rundklammern vergessen oder falsch!")
                return False
        else:
            print("If-Anweisung falsch!")
            return False

    #cond_else    -> 'else' '{' statements '}' | -> ε
    def cond_else(self, syntax_tree):
        elseSet = [token.ELSE]
        openCurlySet = [token.OPEN_CURLY]
        closedCurlySet = [token.CLOSED_CURLY]


        if self.match(elseSet, syntax_tree):
            return self.match(openCurlySet, syntax_tree) and self.statement(syntax_tree.insertSubtree(token.STATEMENT)) and self.match(closedCurlySet, syntax_tree)
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True


    # boolExpression -> termBool righExpressionBool
    def boolExpression(self, syntax_tree):
        return self.termBool(syntax_tree.insertSubtree(token.TERMBOOL)) and self.rightExpressionBool(syntax_tree.insertSubtree(token.RIGHTEXPRBOOL))

    # termBool -> operatorBool rightTermBool
    def termBool(self, syntax_tree):
        return self.operatorBool(syntax_tree.insertSubtree(token.OPERATORBOOL)) and self.rightTermBool(syntax_tree.insertSubtree(token.RIGHTTERMBOOL))

    # operatorBool -> '(' boolExpression ')' | var_bool | identifier | var_num | var_string
    def operatorBool(self, syntax_tree):
        openParaSet = [token.OPEN_PARA]
        closedParaSet = [token.CLOSED_PARA]
        identifierSet = [token.IDENTIFIER]
        boolSet = [token.VAR_BOOL]
        numSet = [token.VAR_NUM]
        stringSet = [token.VAR_STRING]

        if self.match(openParaSet, syntax_tree):
            if self.boolExpression(syntax_tree.insertSubtree(token.BOOLEXPR)):
                if self.match(closedParaSet, syntax_tree):
                    return True
                else:
                    print("Rundklammern vergessen!")
                    return False
        elif self.match(identifierSet, syntax_tree):
            return True
        elif self.match(boolSet, syntax_tree):
            return True
        elif self.match(numSet, syntax_tree):
            return True
        elif self.match(stringSet, syntax_tree):
            return True
        else:
            return False


    #rightTermBool -> '&&' operatorBool rightTermBool  | '||' operatorBool rightTermBool | rightTerm -> '>' operator rightTerm | rightTerm -> '<' operator rightTerm  | ε
    def rightTermBool(self, syntax_tree):
        compOpSet = [token.AND_LOGIC, token.OR_LOGIC]
        gtstOpSet = [token.SMALLER_THAN, token.GREATER_THAN]

        if self.match(compOpSet, syntax_tree):
            return self.operatorBool(syntax_tree.insertSubtree(token.OPERATORBOOL)) and self.rightTermBool(syntax_tree.insertSubtree(token.RIGHTTERMBOOL))
        elif self.match(gtstOpSet, syntax_tree):
            return self.operatorBool(syntax_tree.insertSubtree(token.OPERATORBOOL)) and self.rightTermBool(syntax_tree.insertSubtree(token.RIGHTTERMBOOL))
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True

    # rightExpressionBool -> '==' termBool rightExpressionBool | ‘!=' termBool rightExpressionBool | ε
    def rightExpressionBool(self, syntax_tree):
        compOpSet = [token.IS_EQUAL, token.IS_NOT_EQUAL]
        if self.match(compOpSet, syntax_tree):
            return self.termBool(syntax_tree.insertSubtree(token.TERMBOOL)) and self.rightExpressionBool(syntax_tree.insertSubtree(token.RIGHTEXPRBOOL))
        else:
            syntax_tree.insertSubtree(token.EPSILON)
            return True

    # ReturnStatement -> 'return' var_num | 'return' var_bool | 'return' var_string
    def return_statement(self, syntax_tree):
        varSet = [token.VAR_BOOL, token.VAR_NUM, token.VAR_STRING, token.IDENTIFIER]
        return self.match([token.RETURN], syntax_tree) and self.match(varSet, syntax_tree)

    # applicationStatement -> identifier '(' parameter ')'
    def application_statement(self, syntax_tree):

        identifierSet = [token.IDENTIFIER]
        openParaSet = [token.OPEN_PARA]
        closedParaSet = [token.CLOSED_PARA]

        return self.identifier(syntax_tree) and self.match(openParaSet, syntax_tree) and self.parameter(syntax_tree.insertSubtree(token.PARAMETER)) and self.match(closedParaSet, syntax_tree)
