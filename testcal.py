import environment
import functions
curr_line = 0
tokens = (
    'NAME','NUMBER','FLOAT',
    'PLUS','MINUS','TIMES','DIVIDE',
    'EQUALS', 'LARGER', 'LESS',
    'LCURL', 'RCURL', 'LBRACK', 'RBRACK',
    'LPAREN','RPAREN','SCOLON','COMMA',
    )

# Tokens

t_RCURL  = r'}'
t_LCURL  = r'{'
t_RBRACK  = r'\]'
t_LBRACK  = r'\['
t_SCOLON  = r';'
t_COMMA   = r'\,'
t_LARGER  = r'>'
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

# dictionary of functions
funcs = {}
# test function
functionl = {}
sum_ = functions.function('sum', 'int', parameters=[{'type':'int','name': 'x'}, {'type':'int', 'name':'y'}], line=17)
functionl['sum'] = sum_

next_line = 0
increments = {}
env = environment.environment(-1, name='main')

def function_call(func, params=None, ret=-1):
    global env
    if params is None:
        if func.num == 0:
            env = env.new_env(name=func.name, ret=ret)
            next_line = func.line
            return
        print('function not found')
        return
    else:
        if isinstance(params, list):
            if len(params) == func.num:
                env = env.new_env(name=func.name, ret=ret)
                for i in range(func.num):
                    env.dec_variable(func.parameters[i]['name'],
                                     func.parameters[i]['type'], line=curr_line)
                    env.set_variable(func.parameters[i]['name'], params[i], line=curr_line)
            else:
                print('function not found')
                return
        else:
            env = env.new_env(name=func.name, ret=ret)
            env.dec_variable(func.parameters[i]['name'],
                             func.parameters[i]['type'], line=curr_line)
            env.set_variable(func.parameters[i]['name'], params, line=curr_line)



def p_statement_declare(t):
    '''statement : NAME NAME SCOLON
                 | NAME TIMES NAME SCOLON
                 | NAME NAME LBRACK expression RBRACK SCOLON'''
    print('statement declaration')
    global env
    if t[2] == '*':
        env.dec_variable(t[3], t[1] + '*', line=curr_line)
    elif t[3] == '[':
        env.dec_variable(t[2], t[1] + '*', num = t[4], line=curr_line)
    else:
        if t[1] == 'return':
            env = env.return_func(env.get_variable(t[2]))
        else:
            env.dec_variable(t[2], t[1])


def p_statement_assign(t):
    '''statement : NAME EQUALS expression SCOLON
                 | NAME LBRACK expression RBRACK EQUALS expression SCOLON
                 | NAME LBRACK expression RBRACK EQUALS NAME LPAREN expression RPAREN SCOLON
                 | NAME EQUALS NAME LPAREN expression RPAREN SCOLON'''
    print('statement assignment')
    global env
    if t[2] == '[':
        if t[7] == '(':
            if t[6] in functionl:
                func = functionl[t[6]]
            else:
                return
            parent, _ = env.find_name(t[1] + '[' + str(t[3]) + ']')
            function_call(func, params=t[8], ret=parent.addr)
        else:
            env.set_address(env.get_variable(t[1]) + 4 * t[3], t[6], line=curr_line)
    elif t[4] == ';':
        env.set_variable(t[1], t[3], line=curr_line)
    else:
        if t[3] in functionl:
            func = functionl[t[3]]
        else:
            return
        parent, _ =  env.find_name(t[1])
        function_call(func, params=t[5], ret=parent.addr)


def p_statement_expr(t):
    'statement : expression SCOLON'
    print('statement - expression')
    # end of line process
    for i in increments:
        if increments[i] > 0:
            env.set_variable(i, env.get_variable(i) + increments[i], line=curr_line)
            increments[i] = 0
    if next_line != 0:
        print(next_line)
    print(t[1])

def p_return_call(t):
    '''statement : NAME expression SCOLON'''
    global env
    env = env.return_func(t[2])
    return

def p_function_call(t):
    ''' expression : NAME LPAREN expression RPAREN'''
    global env
    if t[1] in functionl:
        func = functionl[t[1]]
    else:
        print('Function not defined: ' + t[1])
        return
    function_call(func, params=t[3])
    print(t[3])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LARGER expression
                  | expression LESS expression'''
    print('expression binary operation')
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
    elif t[2] == '<':
        t[0] = t[1] < t[3]

def p_postplusplus(t):
    '''expression : NAME PLUS PLUS'''
    print('plpl')
    t[0] = env.get_variable(t[1])
    increments[t[1]] = 1

def p_preplusplus(t):
    '''expression : PLUS PLUS NAME'''
    env.set_variable(t[3], env.get_variable(t[3]) + 1, line=curr_line)
    t[0] = env.get_variable(t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_number(t):
    '''expression : NUMBER
                  | FLOAT'''
    t[0] = int(t[1])


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = env.get_variable(t[1])
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_expression_array(t):
    ''' expression : NAME LBRACK expression RBRACK'''
    parent, _ = env.find_name(t[1])
    if parent.num > t[3]:
        t[0] = env.get_variable(t[1] + '[' + str(t[3]) + ']')
    else:
        print('cannot access beyond allocated array')


def p_comma_sep(t):
    '''expression : expression COMMA expression'''
    if isinstance(t[3], list):
        t[3].insert(0, t[1])
        t[0] = t[3]
    else:
        result = list()
        result.append(t[1])
        result.append(t[3])
        t[0] = result


def p_error(t):
    try:
        print("Syntax error at '%s'" % t.value)
    except:
        print("FAILED!")
        print(t)
        # print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc(debug=True)

while(True):
    s = input(str(curr_line) + '\t>')
    if s == 'exit':
        exit()
    elif s[:5] == 'trace':
        s = s.split(' ')
        env.trace_name(s[1])
    elif s == 'env':
        print(env)
        # print(env.names)
    else:
        parser.parse(s)
        curr_line += 1
