FUNCTION = ";FUNCTION "
POP_VARIABLE = ";POP VARIABLE "
PUSH_CONSTANT = ";PUSH CONSTANT "
PUSH_VARIABLE = ";PUSH VARIABLE "
RETURN = ";RETURN"
CALL = ";CALL "

MUL = ";MUL"
DIV = ";DIV"
ADD = ";ADD"
SUB = ";SUB"

OR = ";OR"
AND = ";AND"

ST = ";ST"
GT = ";GT"
GOFALSE = ";GOFALSE"
GOTRUE = ";GOTRUE"
LABEL = ";LABEL"


class magic_machine():
    
    
    def __init__(self, vm_code):
        self.ip = 0 #instruction pointer
        self.code_memory = vm_code.split(";")[1:]
        print(self.code_memory)
        self.label_table = []
        self.build_label_table()
        self.stack = []
        self.symbol_table = []
        

    ################ stack methoden #####################

    def push_stack(self, value):
        self.stack.insert(0, value)

    def pop_stack(self):
        val = self.stack[0]
        self.stack.pop(0)
        return val

    def get_stack(self):
        return self.stack

    
    ############### symboltabellen methoden #############

    def add_to_symbol_table(self, id, value):
        self.symbol_table.append([id,value])

    def get_value_of_id(self, id):
        for symbol in self.symbol_table:
            if symbol[0] == id:
                return symbol[1]
        return None

    def get_symbol_table(self):
        return self.symbol_table


    ############## labeltabellen methoden ################

    def build_label_table(self):
        for cnt, cmd in enumerate(self.code_memory):
            if LABEL[1:] in cmd:
                self.add_to_label_table(cmd[6:], cnt)

    def add_to_label_table(self, label, pos):
        self.label_table.append([label, pos])

    def get_label_position(self, label):
        for lbls in self.label_table:
            if lbls[0] == label:
                return lbls[1]
        return None

    def get_label_table(self):
        return self.label_table

    ################ vm methoden ########################

    def run(self):

        while self.ip < len(self.code_memory):
            self.interpret(self.code_memory[self.ip])
            self.ip = self.ip + 1

    def interpret(self, code):
        #print(code)
        if PUSH_CONSTANT[1:-1] in code:
           
            self.push_stack(code[len(PUSH_CONSTANT[1:]):])
        elif POP_VARIABLE[1:-1] in code:
            val = self.pop_stack()
            self.add_to_symbol_table(code[len(POP_VARIABLE[1:]):], val)
        elif PUSH_VARIABLE[1:-1] in code:
            val = self.get_value_of_id(code[len(PUSH_VARIABLE[1:]):])
            if val == None:
                print("No such variable initialized: " + code[len(PUSH_VARIABLE[1:]):])
                exit(-1)
            self.push_stack(val)
        elif MUL[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            result = int(val1) * int(val2)
            self.push_stack(result)
        elif DIV[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            result = int(val1) / int(val2)
            self.push_stack(result)
        elif ADD[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            result = int(val1) + int(val2)
            self.push_stack(result)
        elif SUB[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            result = int(val1) - int(val2)
            self.push_stack(result)
        elif AND[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            result = int(val1) and int(val2)
            self.push_stack(result)
        elif OR[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            result = int(val1) or int(val2)
            self.push_stack(result)
        elif ST[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            if int(val1) < int(val2):
                self.push_stack(1)
            else:
                self.push_stack(0)
        elif GT[1:] in code:
            val2 = self.pop_stack()
            val1 = self.pop_stack()
            if int(val1) > int(val2):
                self.push_stack(1)
            else:
                self.push_stack(0)
        elif GOFALSE[1:] in code:
            val = self.pop_stack()
            if val == 0:
                new_ip = self.get_label_position(code[8:])
                self.ip = int(new_ip)
        elif GOTRUE[1:] in code:
            val = self.pop_stack()
            if val == 1:
                new_ip = self.get_label_position(code[7:])
                self.ip = int(new_ip)
        elif FUNCTION[1:] in code:
            pass
        elif RETURN[1:] in code:
            print(code)