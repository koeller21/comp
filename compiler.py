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

    def compile(self, program_file):    
        scan = scanner.Scanner()
        tokenstream = scan.read_program(program_file)
        print(tokenstream)
        if tokenstream != False:
            token_head = scan.create_tokens(tokenstream)
            
            syntax_tree = SyntaxTree(token.MAGICCODE)
            
            parser = Parser(token_head)
            
            p = parser.statement(syntax_tree.insertSubtree("STATEMENT"))

            syntax_tree.printSyntaxTree(0)

            vm_code = Semantic(syntax_tree).generate()
            
            vm = magic_machine(vm_code)
            vm.run()
            
            print(vm.get_symbol_table())
            print(vm.get_stack())
            print(vm.get_label_table())
			


def main():

    comp = Compiler()
    args = comp.parseArguments()
    comp.compile(args.file)


if __name__=="__main__":
    main()

