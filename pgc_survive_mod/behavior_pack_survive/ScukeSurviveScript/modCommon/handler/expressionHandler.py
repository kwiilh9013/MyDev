import re

OPERATORS = {
    '||': 0,
    '&&': 1,
    '<': 2, '<=': 2, '>': 2, '>=': 2, '==': 2, '!=': 2,
    '|': 3,
    '&': 4,
    '+': 5, '-': 5,
    '*': 6, '/': 6,
    '^': 7,
    '!': 8
}

def tokenize(expression):
	return re.findall(r'\d+\.\d+|\d+|[\+\-\*\/]|\|\||\&\&|==|!=|>=|<=|>|<|!|[@\.a-zA-Z\d]+', expression)


def parse_expression(tokens, data):
	return parse_logical_or(tokens, data)


def parse_logical_or(tokens, data):
	left = parse_logical_and(tokens, data)
	while tokens and tokens[0] == '||':
		tokens.pop(0)
		right = parse_logical_and(tokens, data)
		left = bool(left) or bool(right)
	return left


def parse_logical_and(tokens, data):
	left = parse_comparison(tokens, data)
	while tokens and tokens[0] == '&&':
		tokens.pop(0)
		right = parse_comparison(tokens, data)
		left = bool(left) and bool(right)
	return left


def parse_comparison(tokens, data):
	left = parse_or(tokens, data)
	while tokens and tokens[0] in ('>', '<', '>=', '<=', '==', '!='):
		op = tokens.pop(0)
		right = parse_or(tokens, data)
		if op == '>':
			left = left > right
		elif op == '<':
			left = left < right
		elif op == '>=':
			left = left >= right
		elif op == '<=':
			left = left <= right
		elif op == '==':
			left = left == right
		elif op == '!=':
			left = left != right
	return left


def parse_or(tokens, data):
	left = parse_and(tokens, data)
	while tokens and tokens[0] == '|':
		tokens.pop(0)
		right = parse_and(tokens, data)
		left = int(left) | int(right)
	return left


def parse_and(tokens, data):
	left = parse_addition(tokens, data)
	while tokens and tokens[0] == '&':
		tokens.pop(0)
		right = parse_addition(tokens, data)
		left = int(left) & int(right)
	return left


def parse_addition(tokens, data):
	left = parse_multiplication(tokens, data)
	while tokens and tokens[0] in ('+', '-'):
		op = tokens.pop(0)
		right = parse_multiplication(tokens, data)
		if op == '+':
			left += right
		else:
			left -= right
	return left


def parse_multiplication(tokens, data):
	left = parse_exponent(tokens, data)
	while tokens and tokens[0] in ('*', '/'):
		op = tokens.pop(0)
		right = parse_exponent(tokens, data)
		if op == '*':
			left *= right
		else:
			left /= right
	return left


def parse_exponent(tokens, data):
	left = parse_not(tokens, data)
	if tokens and tokens[0] == '^':
		tokens.pop(0)
		right = parse_exponent(tokens, data)
		return left ** right
	return left

def parse_not(tokens, data):
	if tokens and tokens[0] == '!':
		tokens.pop(0)
		return not bool(parse_not(tokens, data))
	return parse_number(tokens, data)

def parse_number(tokens, data):
	if not tokens:
		raise ValueError("Unexpected end of expression")
	token = tokens.pop(0)
	if token == '(':
		result = parse_expression(tokens, data)
		if not tokens or tokens.pop(0) != ')':
			raise ValueError("Unmatched parentheses")
		return result
	try:
		if token[0] == '@':
			if token in data:
				ret = data[token]()
				return ret
			return False
		return float(token)
	except ValueError:
		raise ValueError("Invalid token: %r" % tokens)

def evaluate(expression, data):
	tokens = tokenize(expression)
	return parse_expression(tokens, data)
