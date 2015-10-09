import sys
import lex

tokens = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'NUMBER', 'FLOAT',
          'EQ', 'NE', 'NOT', 'LT', 'GT', 'LE', 'GE', 'ASSIGN',
          'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSHIFT', 'RSHIFT',
          'SEMICOLON', 'RETURN', 'IF', 'ELSE', 'FOR', 'WHILE', 'DO',
          'INT', 'STRING', 'EXTERN', 'NAME',
          'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN']

t_ignore = ' \t\n'

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'

t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='

t_EQ =  r'=='
t_NE =  r'!='
t_NOT = r'!'
t_LT =  r'<'
t_GT =  r'>'
t_LE =  r'<='
t_GE =  r'>='

t_ASSIGN = r'='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LBRACE = r'{'
t_RBRACE = r'}'

t_SEMICOLON = r';'

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_INT(t):
    r'int'
    return t

def t_STRING(t):
    r'string'
    return t

def t_EXTERN(t):
    r'extern'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = float(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

if __name__ == '__main__':
    lexer = lex.lex()
    lex.input(sys.stdin.read())
    while True:
        t = lex.token()
        if not t:
            break
        print t

