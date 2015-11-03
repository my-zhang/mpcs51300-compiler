import sys
import pprint

import ply.lex as lex
import ply.yacc as yacc

pp = pprint.PrettyPrinter(indent=4, width=120)

D = {}

# Reserved words
reserved = ('INT', 'STRING')

tokens = reserved + (
    # Literals (identifier)
    'ID',

    # Delimeters ( ) , ;
    'LPAREN', 'RPAREN', 'COMMA','SEMI',
    )

# Completely ignored characters
t_ignore           = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_COMMA            = r','
t_SEMI             = r';'

# Identifiers and reserved words

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    return t

def t_error(t):
    print "Illegal character %s" % repr(t.value[0])
    t.lexer.skip(1)
    

def p_statement_1(t):
    '''
    statement : declaration
    '''
    t[0] = [t[1]]

def p_statement_2(t):
    '''
    statement : declaration statement 
    '''
    t[0] = [t[1]] + t[2]

def p_declaration_1(t):
    '''
    declaration : type_specifier ID LPAREN RPAREN SEMI
    '''
    t[0] = t[1], t[2], []
    name = t[2]
    if name in D:
        raise ValueError('func define conflit "%s".' %(name))
    D[name] = t[0]

def p_declaration_2(t):
    '''
    declaration : type_specifier ID LPAREN parameter_list RPAREN SEMI
    '''
    t[0] = t[1], t[2], t[4]
    key = '%s$%s' %(t[2], '-'.join(map(lambda p: p[0], t[4])))
    if key in D:
        raise ValueError('func define conflit "%s".' %(key))
    D[key] = t[0]

def p_parameter_list_1(t):
    'parameter_list : parameter_declaration'
    t[0] = [t[1]]

def p_parameter_list_2(t):
    'parameter_list : parameter_list COMMA parameter_declaration'
    t[0] = t[1] + [t[3]]

def p_parameter_declaration(t):
    'parameter_declaration : type_specifier ID'
    t[0] = t[1], t[2]

def p_type_specifier(t):
    '''
    type_specifier : INT 
                   | STRING
    '''
    t[0] = t[1]

lexer = lex.lex(optimize=1)
parser = yacc.yacc(method='LALR')

if __name__ == "__main__":
    s = sys.stdin.read()
    pp.pprint(parser.parse(s))
