class variable:
    type = 'N/A'
    value = 0
    def __init__(self, type, value=0):
        self.type = type
        self.value = value
        self.address = get_new_address()

class environment:
    return_addr = 0
    def __init__(self, return_addr, PARAMS=[]):
        self.return_addr = return_addr
        self.

    def find_var_named(name):


class interpreter:
    # names : list of dictionary
    names = {}

    # stack of environments
    env = []

    def __init__(self):
        print('INTERPRETER ON')
    def


tokens = (
    'NAME','NUMBER','FLOAT',
    'PLUS','MINUS','TIMES','DIVIDE',
    'EQUALS', 'EQLARGER', 'LARGER', 'LESS', 'EQLESS',
    'LPAREN','RPAREN','SCOLON','COMMA',
    )

# Tokens

t_SCOLON  = r';'
t_COMMA   = r'\,'
t_EQLARGER= r'>='
t_LARGER  = r'>'
t_EQLESS  = r'<='
t_LESS    = r'<'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_FLOAT(t):
    r'-?\d+\.\d'
    try:
        t.value = float(t.value)
    except ValueError:
        print('error haha')
        t.value = 0
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
    )

# dictionary of names
names = {}

# dictionary of functions
funcs = {}


def p_statement_declare(t):
    '''statement : NAME NAME
                 | NAME names'''
    names[t[2]] = {'type': t[1], 'value': 'None'}


def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    type_ = names[t[1]]['type']
    print(type_)
    if type_ == 'int':
        if type(t[3]) == int:
            names[t[1]]['value'] = t[3]
        else:
            if type(t[3]) == float:
                if int(t[3]) == t[3]:
                    names[t[1]]['value'] = int(t[3])
                else:
                    print('Type error, implicit cast invalid: float to int')
                    print(str(t[3]) + ' to int not valid')
            else:
                print('Invalid type. Cannot assign ' + type + ' to an Integer')
    if type_ == 'float':
        print(type(t[3]))
        if type(t[3]) == float:
            names[t[1]]['value'] = t[3]
        else:
            try:
                names[t[1]]['value'] = float(t[3])
            except:
                print('Invalid type. Cannot assign ' + type + ' to a Float')


def p_function_def(t):
    'expression : NAME NAME LPAREN expression RPAREN'
    for i in t:
        print(i)


def p_statement_expr(t):
    'statement : expression'
    print(t[1])


def p_names(t):
    '''names : NAME COMMA NAME
             | NAME COMMA names
             | NAME'''
    try:
        t[3].insert(0, t[1])
        t[0] = t[3]
    except:
        if len(t) == 4:
            result = list()
            result.append(t[1])
            result.append(t[3])
            t[0] = result
        else:
            t[0] = [t[1]]


def p_func(t):
    'expression : NAME LPAREN names RPAREN'
    print('FUNCTION CALL')
    if t[1] == 'print':
        print(t[3])
    elif t[1] == 'float':
        t[0] = (float(t[3]))
    elif t[1] == 'int':
        t[0] = (int(t[3]))


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQLESS expression
                  | expression EQUALS EQUALS expression
                  | expression EQLARGER expression
                  | expression LARGER expression
                  | expression LESS expression'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '>':
        t[0] = t[1] > t[3]
    elif t[2] == '>=':
        t[0] = t[1] >= t[3]
    elif t[2] == '==':
        t[0] = t[1] == t[3]


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    '''expression : NUMBER
                  | FLOAT'''
    t[0] = t[1]


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_expression_names(t):
    'expression : expression COMMA expression'
    t[1].append([t[3]])
    t[0] = t[1]

def p_error(t):
    try:
        print("Syntax error at '%s'" % t.value)
    except:
        print("FAILED!")
        print(t)
        # print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc(debug=True)


def interpret_line(s):
    parser.parse(s)
