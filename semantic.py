import magic_machine
import token


class Semantic():

	def __init__(self, syntax_tree):
		self.st = syntax_tree
		self.label_counter = 0

	def create_label(self):
		new_lbl = " L" + str(self.label_counter)
		self.label_counter = self.label_counter + 1
		return new_lbl

	####################### Code generator ######################################

	def generate(self):

		if self.st.get_token() == "MAGICCODE":
			return str(self.semantic_statement(self.st.children[0], ""))
		else:
			return None

	def semantic_statement(self, top, n):
		#print(top.children)
		#print(top.children[0].get_token())
		if len(top.children) == 3:
			nxt_stmt = top.children[0]
			semicolon = top.children[1]
			stmt = top.children[2]

			# print(nxt_stmt.get_token())
			# print(nxt_stmt.get_value())
			# print(semicolon.get_token())
			# print(semicolon.get_value())
			
			# print(stmt.get_token())
			# print(stmt.get_value())

			if nxt_stmt.get_token() == "ASSIGNMENT":
				return n + self.semantic_statement(stmt, self.assignment_statement(nxt_stmt))
			if nxt_stmt.get_token() == "APPLICATION":
				return n + self.semantic_statement(stmt, self.semantic_application_statement(nxt_stmt))

		elif len(top.children) == 2:
			nxt_stmt = top.children[0]
			stmt = top.children[1]

			if nxt_stmt.get_token() == "CONDITIONAL":
				return n + self.semantic_statement(stmt, self.semantic_condition(nxt_stmt))
			if nxt_stmt.get_token() == "FUNCTIONDEF":
				return n + self.semantic_statement(stmt, self.semantic_function_definition(nxt_stmt))
			if nxt_stmt.get_token() == "RETURN":
				return n + self.semantic_return(nxt_stmt)
		elif len(top.children) == 1:
			nxt_stmt = top.children[0]
			if nxt_stmt.get_token() == "EPSILON":
				return n

	def assignment_statement(self, top):

		identifier = top.children[0]
		equals = top.children[1]
		val = top.children[2]

		if val.get_token() == "EXPRESSION":
			return self.semantic_expression(val) + magic_machine.POP_VARIABLE + self.semantic_identifier(identifier)
		elif val.get_token() == "VAR_STRING":
			return "" #TODO
		elif val.get_token() == "APPLICATION":
			return self.semantic_application_statement(val) + magic_machine.POP_VARIABLE + self.semantic_identifier(identifier)
		elif val.get_token() == "IDENTIFIER":
			return magic_machine.PUSH_VARIABLE + self.semantic_identifier(val) + magic_machine.POP_VARIABLE + self.semantic_identifier(identifier)
		elif val.get_token() == "BOOLEXPR":
			return self.semantic_bool_expression(val) + magic_machine.POP_VARIABLE + self.semantic_identifier(identifier)

	################################# fuer arithmetische ausdruecke ######################################
	def semantic_expression(self, top):
		term = top.children[0]
		rightExpression = top.children[1]
		return self.semantic_rightExpression(rightExpression, self.semantic_term(term))

	def semantic_term(self, top):
		operator = top.children[0]
		rightTerm = top.children[1]
		return self.semantic_rightTerm(rightTerm, self.semantic_operator(operator))

	def semantic_operator(self, top):
		if len(top.children) == 1:
			if top.children[0].get_token() == token.VAR_NUM:
				var_num = top.children[0]
				return magic_machine.PUSH_CONSTANT + self.semantic_var_num(var_num)
			elif top.children[0].get_token() == token.IDENTIFIER:
				identifier = top.children[0]
				return magic_machine.PUSH_VARIABLE + self.semantic_identifier(identifier)
		elif len(top.children) == 3:
			open_para = top.children[0]
			expression = top.children[1]
			closed_para = top.children[2]
			return self.semantic_expression(expression)

	def semantic_var_num(self, top):
		return str(top.get_value())

	def semantic_rightTerm(self, top, n):

		if len(top.children) == 1:
			return n
		elif len(top.children) == 3:
			op = top.children[0]
			operator = top.children[1]
			rightTerm = top.children[2]
			if op.get_token() == token.MUL: #{ rightTerm.f(z) = z * rightTerm.f(operator.f(z)) }
				return n + self.semantic_rightTerm(rightTerm, self.semantic_operator(operator)) + magic_machine.MUL
			elif op.get_token() == token.DIV: #{ rightTerm.f(z) = z / rightTerm.f(operator.f(z)) }
				return n + self.semantic_rightTerm(rightTerm, self.semantic_operator(operator)) + magic_machine.DIV


	def semantic_rightExpression(self, top, n):
		if len(top.children) == 1:
			return n
		elif len(top.children) == 3:
			op = top.children[0]
			term = top.children[1]
			rightExpression = top.children[2]
			if op.get_token() == token.PLUS: # rightExpression.f(z) = z + rightExpression.f(term.f(z2))
				return n + "" + self.semantic_rightExpression(rightExpression, self.semantic_term(term)) + magic_machine.ADD
			elif op.get_token() == token.MINUS: # rightExpression.f(z) = z - rightExpression.f(term.f(z2))
				return n + "" + self.semantic_rightExpression(rightExpression, self.semantic_term(term)) + magic_machine.SUB

	def semantic_identifier(self, top):
		return str(top.get_value())


	############################### fuer boolsche ausdruecke ##################################################

	#  { boolExpression.f(z) = rightExprbool.f(termbool.f(z)) }
	def semantic_bool_expression(self, top):
		termbool = top.children[0]
		rightexprbool = top.children[1]
		return self.semantic_rightExprBool(rightexprbool, self.semantic_termBool(termbool))

	# { rightExprbool.f(z) = z == rightExprbool.f(termbool.f(z2)) }
	def semantic_rightExprBool(self, top, n):
		if len(top.children) == 1:
			return n
		elif len(top.children) == 3:
			op = top.children[0]
			termBool = top.children[1]
			rightExprBool = top.children[2]
			if op.get_token() == token.IS_EQUAL:
				return n + "" + self.semantic_rightExprBool(rightExprBool, self.semantic_term(termBool)) + magic_machine.EQ
			elif op.get_token() == token.IS_NOT_EQUAL:
				return n + "" + self.semantic_rightExprBool(rightExprBool, self.semantic_term(termBool)) + magic_machine.NEQ

	#  { termbool.f(z) = rightTermBool.f(operatorbool.f(z))  }
	def semantic_termBool(self, top):
		operatorBool = top.children[0]
		rightTermBool = top.children[1]
		return self.semantic_rightTermBool(rightTermBool, self.semantic_operatorBool(operatorBool))

	# { operatorbool.f(z) = ( boolExpression.f(z) ) } {operatorbool.f(z) = var_num.f(z)} {operatorbool.f(z) = identifier.f(z)}
	# { operatorbool.f(z) = var_bool.f(z)} {var_bool.f(z) = true | false}
	def semantic_operatorBool(self, top):

		if len(top.children) == 1:
			if top.children[0].get_token() == token.VAR_BOOL:
				var_bool = top.children[0]
				return magic_machine.PUSH_CONSTANT + self.semantic_var_bool(var_bool)
			elif top.children[0].get_token() == token.VAR_NUM:
				var_num = top.children[0]
				return magic_machine.PUSH_CONSTANT + self.semantic_var_num(var_num)
			elif top.children[0].get_token() == token.IDENTIFIER:
				identifier = top.children[0]
				return magic_machine.PUSH_VARIABLE + self.semantic_identifier(identifier)
		elif len(top.children) == 3:
			open_para = top.children[0]
			bool_expression = top.children[1]
			closed_para = top.children[2]
			return self.semantic_bool_expression(bool_expression)

	# { rightTermBool.f(z) = z && rightTermBool.f(operatorbool.f(z)) }
	def semantic_rightTermBool(self, top, n):
		if len(top.children) == 1:
			return n
		elif len(top.children) == 3:
			op = top.children[0]
			operatorBool = top.children[1]
			rightTermBool = top.children[2]
			if op.get_token() == token.AND_LOGIC:
				return n + self.semantic_rightTermBool(rightTermBool, self.semantic_operatorBool(operatorBool)) + magic_machine.AND
			elif op.get_token() == token.OR_LOGIC:
				return n + self.semantic_rightTermBool(rightTermBool, self.semantic_operatorBool(operatorBool)) + magic_machine.OR
			elif op.get_token() == token.GREATER_THAN:
				return n + self.semantic_rightTermBool(rightTermBool, self.semantic_operatorBool(operatorBool)) + magic_machine.GT
			elif op.get_token() == token.SMALLER_THAN:
				return n + self.semantic_rightTermBool(rightTermBool, self.semantic_operatorBool(operatorBool)) + magic_machine.ST

	def semantic_var_bool(self, top):
		if top.get_value() == "true":
			return str(1)
		else:
			return str(0)


	############################### fuer if ausdruecke ################################################
	# conditional  -> 'if' '(' boolExpression ')' '{' statements '}' cond_else
	# cond_else    -> 'else' '{' statements '}'
	#              -> ε

	def semantic_condition(self, top):
		a_if = top.children[0]
		open_para = top.children[1]
		bool_expr = top.children[2]
		closed_para = top.children[3]
		open_curly = top.children[4]
		stmt = top.children[5]
		closed_curly = top.children[6]
		cond_else = top.children[7]

		lbl = self.create_label()
		lbl2 = self.create_label()

		return self.semantic_bool_expression(bool_expr) + magic_machine.GOFALSE + lbl + self.semantic_statement(stmt, "") +  \
				magic_machine.LABEL + lbl + self.semantic_bool_expression(bool_expr) + magic_machine.GOTRUE + lbl2 + \
				self.semantic_cond_else(cond_else) + magic_machine.LABEL + lbl2

	def semantic_cond_else(self, top):
		if len(top.children) == 1 :
			return ""
		else:
			p_else = top.children[0]
			open_curly = top.children[1]
			stmt = top.children[2]
			closed_curly = top.children[3]

			return self.semantic_statement(stmt, "")

	# FunctionDefinition -> 'magic' identifier '(' arguments ')' '{' statement '}'
	#            arguments -> identifier R
	#                      -> ε
	#            R -> ',' arguments R
	#              -> ε

	def semantic_function_definition(self, top):


		magic = top.children[0]
		identifier = top.children[1]
		open_para = top.children[2]
		argument = top.children[3]
		closed_para = top.children[4]
		open_curly = top.children[5]
		stmt = top.children[6]
		closed_curly = top.children[7]


		return magic_machine.FUNCTION + self.semantic_identifier(identifier) + self.semantic_argument(argument) + self.semantic_statement(stmt, "") + magic_machine.RETURN

	def semantic_argument(self, top):
		if len(top.children) == 2:
			identifier = top.children[0]
			arg_r = top.children[1]
			return magic_machine.POP_VARIABLE + self.semantic_arg_r(arg_r, self.semantic_identifier(identifier))
		elif len(top.children) == 1:
			return ""

	def semantic_arg_r(self, top, n):

		if len(top.children) == 3:

			comma = top.children[0]
			argument = top.children[1]
			arg_r = top.children[2]

			return n + self.semantic_arg_r(arg_r, self.semantic_argument(argument))

		elif len(top.children) == 1:
			return n

	# ReturnStatement -> 'return' var_num | 'return' var_bool | 'return' var_string | 'return' identifier
	def semantic_return(self, top):
		print(top.children)

		if len(top.children) == 2:
			return_stmt = top.children[0]
			var = top.children[1]

			if var.get_token() == "IDENTIFIER":
				return magic_machine.PUSH_VARIABLE + self.semantic_identifier(var)
			if var.get_token() == "VAR_NUM":
				return magic_machine.PUSH_CONSTANT + self.semantic_var_num(var)
			if var.get_token() == "VAR_BOOL":
				return magic_machine.PUSH_CONSTANT + self.semantic_var_bool(var)


	# ApplicationStatement -> FunctionName '(' 'parameter' ')'
	#        parameter -> identifier R
	#                  -> ε
	#        R -> ',' parameter R
	#          -> ε
	def semantic_application_statement(self, top):

		function_name = top.children[0]
		open_para = top.children[1]
		parameter = top.children[2]
		closed_para = top.children[3]


		return self.get_and_sort_parameters(parameter) + magic_machine.CALL + self.semantic_identifier(function_name)
	def get_and_sort_parameters(self, parameter):
		paras = self.semantic_parameter(parameter).split(";")[1:][::-1] #baue parameter und kehre reihenfolge um
		paras_str = ""
		for p in paras:
			paras_str = paras_str + ";" + p
		return paras_str

	def semantic_parameter(self, top):
		if len(top.children) == 2:
			identifier = top.children[0]
			r = top.children[1]
			return magic_machine.PUSH_VARIABLE + self.semantic_r(r, self.semantic_identifier(identifier))
		elif len(top.children) == 1:
			return ""

	def semantic_r(self, top, n):

		if len(top.children) == 3:

			comma = top.children[0]
			parameter = top.children[1]
			r = top.children[2]

			return  n + self.semantic_r(r, self.semantic_parameter(parameter))

		elif len(top.children) == 1:
			return n









	#end
