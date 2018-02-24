import re
import filerw
import token


class Scanner(object):

    def __init__(self):
        self.separators = ["{",";","(",")",",","}","*","/","+","-","=","<",">","&&","||", "==", "!="] #TODO da muessen alle hin

    def read_program(self, prog):

        try:
            with open(prog,"r") as content:
                magic_programm = ""
                for line in content:

                    line = line.replace(" ","")
                    line = line.replace("\n","")
                    line = line.replace("\t","")

                    if not line.startswith("#"):
                        magic_programm = magic_programm + line

                tokens = self.tokenize(magic_programm)
                return tokens
        except IOError as e:
            print(e)
            return False

    def tokenize(self, content):
        tokens = []
        q = 0
        for i in range(0,len(content)):

            if content[i] in self.separators:

                if len(content[q:i]) > 0:
                    tokens.append(content[q:i])

                if content[i:i+2] != "==" and content[i-1:i+1] != "==" and content[i-1:i+1] != "!=":
                    tokens.append(content[i:i+1])
                q=i+1

            if content[i:i+2] in self.separators and content[i:i+2] not in [";","}"]:

                if len(content[q:i]) > 0:
                    tokens.append(content[q:i])
                tokens.append(content[i:i+2])
                q=i+2

            if content[i:i+5] == "magic":
                tokens.append(content[i:i+5])
                q=i+5

            if content[i:i+6] == "return":
                tokens.append(content[i:i+6])
                q=i+6

        return tokens

    def create_tokens(self, tokenstream):

        nxt_token = first_token = token.Token(data="",token_type="MAGICCODE",next_token=None)

        for tok in tokenstream:
            if token.getWordToToken(tok) != False:

                t = token.tokenCreator(tok, token.getWordToToken(tok), nxt_token)
                nxt_token = t

            else:
                #print("Falsche Bezeichner!")
                pass

        return first_token
