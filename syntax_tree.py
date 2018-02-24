


from semantic import Semantic

class SyntaxTree(object):
    def __init__(self, token):
        self.token = token
        self.value = ""
        self.children = []

    def insertSubtree(self, token, value=None):
        st = SyntaxTree(token)
        st.set_value(value)
        self.children.append(st)
        return st

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_token(self):
        return str(self.token)

    def printSyntaxTree(self, depth):
        for node in self.children:
            spaces = depth * "\t"
            print(spaces + str(node.get_token()) + " ---> " + str(node.get_value()) )
            node.printSyntaxTree(depth+1)

    def generate_vm_code(self, head):

        return Semantic(head).generate()
