import re

MAGICCODE = "MAGICCODE"
STATEMENT = "STATEMENT"
SEMICOLON = "SEMICOLON"
EPSILON = "EPSILON"
COMMA = "COMMA"
OPEN_PARA = "OPEN_PARA"
CLOSED_PARA = "CLOSED_PARA"
EQUALS = "EQUALS"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
OPEN_CURLY = "OPEN_CURLY"
CLOSED_CURLY = "CLOSED_CURLY"
IS_EQUAL = "IS_EQUAL"
IS_NOT_EQUAL = "IS_NOT_EQUAL"
SMALLER_THAN = "SMALLER_THAN"
GREATER_THAN = "GREATER_THAN"
MAGIC = "MAGIC"
RETURN = "RETURN"


VAR_BOOL = "VAR_BOOL"
VAR_NUM = "VAR_NUM"
IDENTIFIER = "IDENTIFIER"
VAR_STRING = "VAR_STRING"
EXPRESSION = "EXPRESSION"
AND_LOGIC = "AND_LOGIC"
OR_LOGIC = "OR_LOGIC"

CONDITIONAL = "CONDITIONAL"
COND_ELSE = "COND_ELSE"
IF = "IF"
ELSE = "ELSE"

#Syntaxbaumtoken
FUNCTIONDEF = "FUNCTIONDEF"
APPLICATION = "APPLICATION"
ASSIGNMENT = "ASSIGNMENT"
PARAMETER = "PARAMETER"
RIGHTEXPRESSION = "RIGHTEXPRESSION"
RIGHTTERM = "RIGHTTERM"
TERM = "TERM"
OPERATOR= "OPERATOR"
BOOLEXPR = "BOOLEXPR"
TERMBOOL = "TERMBOOL"
RIGHTEXPRBOOL = "RIGHTEXPRBOOL"
OPERATORBOOL = "OPERATORBOOL"
RIGHTTERMBOOL = "RIGHTTERMBOOL"




def getWordToToken(word):
    token_t = ""
    if word == ";":
        token_t = SEMICOLON
    elif word == ",":
        token_t = COMMA
    elif word == "(":
        token_t = OPEN_PARA
    elif word == ")":
        token_t = CLOSED_PARA
    elif word == "=":
        token_t = EQUALS
    elif word == "+":
        token_t = PLUS
    elif word == "-":
        token_t = MINUS
    elif word == "*":
        token_t = MUL
    elif word == "/":
        token_t = DIV
    elif word == "{":
        token_t = OPEN_CURLY
    elif word == "}":
        token_t = CLOSED_CURLY
    elif word == "==":
        token_t = IS_EQUAL
    elif word == "!=":
        token_t = IS_NOT_EQUAL
    elif word == "<":
        token_t = SMALLER_THAN
    elif word == ">":
        token_t = GREATER_THAN
    elif word == "&&":
        token_t = AND_LOGIC
    elif word == "||":
        token_t = OR_LOGIC
    elif word == "magic":
        token_t = MAGIC
    elif word == "return":
        token_t = RETURN
    elif word == "if":
        token_t = IF
    elif word == "else":
        token_t = ELSE
    elif word == "true":
        token_t = VAR_BOOL
    elif word == "false":
        token_t = VAR_BOOL
    elif re.compile("[A-Za-z]").match(word): # Form : abc, ABC, aBc
        token_t = IDENTIFIER
    elif re.compile("^[0-9]*$").match(word): # Form : 021, 21, 9
        token_t = VAR_NUM
    elif re.compile('^"[a-zA-Z0-9\s]*"$').match(word): # Form : "a", "ab", "a9", "9"
        token_t = VAR_STRING
    #elif re.compile('([-+]?[A-Za-z0-9]*\.?[A-Za-z0-9]+[\/\+\-\*])+([-+]?[A-Za-z0-9]*\.?[A-Za-z0-9]+)'): # Form: a + b , 9 - 2, a * 9
    #    token_t = EXPRESSION
    #TODO Else fall

    if token_t != "":
        return token_t
    else:
        return False

def tokenCreator(word, token_type, prev_token):
    t_new = Token(data=word, token_type=token_type)
    prev_token.set_next(t_new)
    return t_new

class Token(object):

    def __init__(self, data=None, token_type=None, next_token=None):
        self.data = data
        self.token_type = token_type
        self.next_token = next_token

    def get_data(self):
        return self.data

    def get_token_type(self):
        return self.token_type

    def get_next(self):
        return self.next_token

    def set_next(self, new_next):
        self.next_token = new_next

    def get(self, org_token, cnt):
        cur_token = org_token
        for i in range(0, cnt):
            cur_token = cur_token.get_next()
        return cur_token
