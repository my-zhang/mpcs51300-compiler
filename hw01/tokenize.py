import sys
import lex

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'for' : 'FOR',
   'do' : 'DO',
   'int' : 'INT',
   'string' : 'STRING',
   'extern' : 'EXTERN',
   'return' : 'RETURN'
}

tokens = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'NUMBER', 'FLOAT',
          'EQ', 'NE', 'NOT', 'LT', 'GT', 'LE', 'GE', 'ASSIGN',
          'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSHIFT', 'RSHIFT',
          'SEMICOLON', 'ID', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 
          'DIV_ASSIGN', 'MOD_ASSIGN']+ list(reserved.values())

t_ignore = ' \t'

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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError("syntax error on line %d near '%s'\n" % (t.lineno, t.value))

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')   
    # t.value = (t.value, symbol_lookup(t.value))
    return t

if __name__ == '__main__':
    lexer = lex.lex()
    lex.input(sys.stdin.read())
    while True:
        t = lex.token()
        if not t:
            break
        print t.value, '\t:\t', t.type

