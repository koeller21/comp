from syntax_tree import SyntaxTree
from magic_parser import Parser
from semantic import Semantic
from magic_machine import magic_machine
import scanner
import token
import argparse # for command line arguments

class Compiler(object):    

    def __init__(self):
        pass

    def parseArguments(self):
        argparser = argparse.ArgumentParser(description="Compiler for the new programming language magic!")
        argparser.add_argument("file", type=str)
        argparser.add_argument("-d","--debug", required=False)   
        return argparser.parse_args()

    def compile(self, program_file, debug_mode):    
        scan = scanner.Scanner()
        tokenstream = scan.read_program(program_file)

        if debug_mode == True: # prints language tokens 
            print("Language tokens : " + str(tokenstream))

        if tokenstream != False:
            token_head = scan.create_tokens(tokenstream)
            
            syntax_tree = SyntaxTree(token.MAGICCODE)
            
            parser = Parser(token_head)
            
            parser.statement(syntax_tree.insertSubtree("STATEMENT"))

            if debug_mode == True: # prints syntax tree generated by parser
                syntax_tree.printSyntaxTree(0)

            vm_code = Semantic(syntax_tree).generate()
            
            vm = magic_machine(vm_code, debug_mode)
            vm.run()

            print("Result : " + str(vm.get_symbol_table()))
                
def main():

    debug_mode = False

    comp = Compiler()
    args = comp.parseArguments()
    
    if args.debug == "true":
        debug_mode = True 
    
    comp.compile(args.file, debug_mode)


if __name__=="__main__":
    main()

