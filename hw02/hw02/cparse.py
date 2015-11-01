import sys
import pprint

import clex
import ply.yacc as yacc

import preprocess
from preprocess import remove_blank
from preprocess import remove_comment

pp = pprint.PrettyPrinter(indent=4, width=120)

# token map
tokens = clex.tokens

# program:

def p_program_1(t):
    'program : external_declaration'
    t[0] = [t[1]]
    return t[0]

def p_program_2(t):
    'program : program external_declaration'
    t[0] = t[1] + [t[2]]
    return t[0]

# external-declaration:

def p_external_declaration_1(t):
    '''external_declaration : function_definition'''
    t[0] = t[1]
    # print 'function_definition',t[0]

def p_external_declaration_3(t):
    '''external_declaration : declaration'''
    t[0] = t[1]
    if(len(t[1][2][0])==2):
        print 'Predefined Function with name',t[1][2][0][0][1]

def p_external_declaration_2(t):
    'external_declaration : EXTERN declaration'
    t[0] = 'EXTERN', t[2]
    print 'Define extern function with name', t[2][2][0][0][1]

# function-definition:
def p_function_definition(t):
    'function_definition : type_specifier declarator compound_statement'
    t[0] = 'FUNC_DEF', t[1], t[2], t[3]
    print 'Define function with name', t[2][0][1]

# declaration:
def p_declaration(t):
    'declaration : type_specifier init_declarator_list SEMI'
    t[0] = 'VAR_DEC', t[1], t[2]
    # print t[0]
    if(t[2][0][0]=='ID'):
        for i in range(len(t[2])):
            print 'Define variable with type',t[1][1],'and name',
            print t[2][i][1]
    elif(t[2][0][1][0]=='ID'):
        print 'Define variable with type',t[1][1],'and name',
        print t[2][0][1][1]
        if((len(t[2][0][2])==2) & (not ((t[1][1]=='int') & (t[2][0][2][0]=='ICONST'))) & (not((t[1][1]=='string') & (t[2][0][2][0]=='SCONST')))):
            p_error(t)


# declaration-list:
def p_declaration_list_1(t):
    'declaration_list : declaration'
    t[0] = [t[1]]

def p_declaration_list_2(t):
    'declaration_list : declaration_list declaration '
    t[0] = t[1] + [t[2]]


# type-specifier:
def p_type_specifier(t):
    '''type_specifier : INT
                      | STRING
                      '''
    t[0] = 'TYPE', t[1]

# init-declarator-list:

def p_init_declarator_list_1(t):
    'init_declarator_list : init_declarator'
    t[0] = [t[1]]
    # print 'init_declarator_list',t[1]

def p_init_declarator_list_2(t):
    'init_declarator_list : init_declarator_list COMMA init_declarator'
    t[0] = t[1] + [t[3]]

# init-declarator

def p_init_declarator_1(t):
    'init_declarator : declarator'
    t[0] = t[1]
    # if(t[0][0]=='ID'):
        # print 'with name',t[0][1]

def p_init_declarator_2(t):
    'init_declarator : declarator EQUALS expression'
    t[0] = 'INIT_ASSIGN', t[1], t[3]

# declarator:

def p_declarator_1(t):
    'declarator : ID'
    t[0] = 'ID', t[1]
    # print 'With name', t[1]

def p_declarator_2(t):
    'declarator : ID LPAREN parameter_type_list RPAREN '
    t[0] = ('ID', t[1]), t[3]
    # print 'parameter_type_list', t[3]

def p_declarator_3(t):
    'declarator : ID LPAREN identifier_list RPAREN '
    t[0] = ('ID', t[1]), t[3]
    # print 'identifier_list', t[3]

def p_declarator_4(t):
    'declarator : ID LPAREN RPAREN '
    t[0] = ('ID', t[1]), None

# pointer:

def p_pointer_1(t):
    'pointer : TIMES'
    pass

def p_pointer_2(t):
    'pointer : TIMES pointer'
    pass


# parameter-type-list:

def p_parameter_type_list_1(t):
    'parameter_type_list : parameter_list'
    t[0] = t[1]

def p_parameter_list_1(t):
    'parameter_list : parameter_declaration'
    t[0] = [t[1]]

def p_parameter_list_2(t):
    'parameter_list : parameter_list COMMA parameter_declaration'
    t[0] = t[1] + [t[3]]

# parameter-declaration:
def p_parameter_declaration(t):
    'parameter_declaration : type_specifier declarator'
    t[0] = t[1], t[2]

# identifier-list:
def p_identifier_list_1(t):
    'identifier_list : ID'
    pass

def p_identifier_list_2(t):
    'identifier_list : identifier_list COMMA ID'
    pass


# statement:

def p_statement(t):
    '''
    statement : expression_statement
              | compound_statement
              | selection_statement
              | iteration_statement
              | jump_statement
              '''
    t[0] = 'STAT', t[1]

# expression-statement:
def p_expression_statement(t):
    'expression_statement : expression_opt SEMI'
    t[0] = t[1]

# compound-statement:

def p_compound_statement_1(t):
    'compound_statement : LBRACE declaration_list statement_list RBRACE'
    t[0] = 'COMP_STATS', t[2] + t[3]

def p_compound_statement_2(t):
    'compound_statement : LBRACE statement_list RBRACE'
    t[0] = 'COMP_STATS', t[2]

def p_compound_statement_3(t):
    'compound_statement : LBRACE declaration_list RBRACE'
    t[0] = 'COMP_STATS', t[2] 

def p_compound_statement_4(t):
    'compound_statement : LBRACE RBRACE'
    t[0] = 'COMP_STATS', []

# statement-list:

def p_statement_list_1(t):
    'statement_list : statement'
    t[0] = [t[1]]

def p_statement_list_2(t):
    'statement_list : statement_list statement'
    t[0] = t[1] + [t[2]]

# selection-statement

def p_selection_statement_1(t):
    # 'selection_statement : IF LPAREN expression RPAREN statement'
    'selection_statement : IF LPAREN condition RPAREN statement'
    t[0] = 'IF', t[3], t[5]
    print 'If Selection on operator',t[3][0]

def p_selection_statement_2(t):
    # 'selection_statement : IF LPAREN expression RPAREN statement ELSE statement '
    'selection_statement : IF LPAREN condition RPAREN statement ELSE statement '
    t[0] = 'IF_ELSE', t[3], t[5], t[7]
    print 'If_Else Selection on operator', t[3][0]

# iteration_statement:
def p_iteration_statement_1(t):
    'iteration_statement : WHILE LPAREN condition RPAREN statement'
    t[0] = 'WHILE', t[3], t[5]
    if(t[3][1][0]=='ID'):
        print 'Define While iteration with variable', t[3][1][1]

def p_iteration_statement_2(t):
    'iteration_statement : FOR LPAREN expression_opt SEMI condition SEMI expression_opt RPAREN statement '
    t[0] = 'FOR', t[3], t[5], t[7], t[9]
    print 'Define Iteration with variable',t[3][1][1]

def p_iteration_statement_3(t):
    'iteration_statement : DO statement WHILE LPAREN condition RPAREN SEMI'
    t[0] = 'DO_WHILE', t[2], t[5]
    if(t[5][1][0]=='ID'):
        print 'Define DO_WHILE iteration with variable', t[5][1][1]

# jump_statement:
def p_jump_statement(t):
    'jump_statement : RETURN expression_opt SEMI'
    t[0] = 'RET', t[2]
    print 'Return ',t[2][1]

def p_expression_opt_1(t):
    'expression_opt : empty'
    t[0] = t[1]

def p_expression_opt_2(t):
    'expression_opt : expression'
    t[0] = t[1]

# expression:

def p_expression_1(t):
    'expression : additive_expression'
    t[0] = t[1]
    # print 'expression',t[0]

def p_expression_2(t):
    'expression : unary_expression assignment_operator expression'
    t[0] = 'ASSIGN', t[1], t[3]
    print 'Assign', t[1][1]

def p_expression_3(t):
    'expression : expression LSHIFT additive_expression'
    t[0] = 'LSHIFT', t[1], t[3]

def p_expression_4(t):
    'expression : expression RSHIFT additive_expression'
    t[0] = 'RSHIFT', t[1], t[3]

# condition
def p_condition(t):
    'condition : expression comparison_operator expression'
    t[0] = t[2], t[1], t[3]
    # print t[0]

def p_comparison_operator(t):
    '''comparison_operator : EQ
                           | NE
                           | LT
                           | GT
                           | LE
                           | GE'''
    t[0] = t[1]

# assignment_operator:
def p_assignment_operator(t):
    '''
    assignment_operator : EQUALS
                        | TIMESEQUAL
                        | DIVEQUAL
                        | MODEQUAL
                        | PLUSEQUAL
                        | MINUSEQUAL
                        '''
    t[0] = t[1]


# additive-expression

def p_additive_expression_1(t):
    'additive_expression : multiplicative_expression'
    t[0] = t[1]

def p_additive_expression_2(t):
    'additive_expression : additive_expression PLUS multiplicative_expression'
    t[0] = 'ADD', t[1], t[3]
    # print 'Addition', t[1][1], 'and', t[3][1][1]

def p_additive_expression_3(t):
    'additive_expression : additive_expression MINUS multiplicative_expression'
    t[0] = 'SUB', t[1], t[3]

# multiplicative-expression

def p_multiplicative_expression_1(t):
    'multiplicative_expression : unary_expression'
    t[0] = t[1]

def p_multiplicative_expression_2(t):
    'multiplicative_expression : multiplicative_expression TIMES unary_expression'
    t[0] = 'MUL', t[1], t[3]

def p_multiplicative_expression_3(t):
    'multiplicative_expression : multiplicative_expression DIVIDE unary_expression'
    t[0] = 'DIV', t[1], t[3]

def p_multiplicative_expression_4(t):
    'multiplicative_expression : multiplicative_expression MOD unary_expression'
    t[0] = 'MOD', t[1], t[3]


# unary-expression:
def p_unary_expression_1(t):
    'unary_expression : postfix_expression'
    t[0] = t[1]

def p_unary_expression_2(t):
    'unary_expression : MINUS unary_expression'
    t[0] = 'NEG', t[2]

# postfix-expression:

def p_postfix_expression_1(t):
    'postfix_expression : primary_expression'
    t[0] = t[1]

def p_postfix_expression_2(t):
    'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
    t[0] = 'FUNC_CALL', t[1], t[3]
    print 'Call Function',t[1][1]

def p_postfix_expression_3(t):
    'postfix_expression : postfix_expression LPAREN RPAREN'
    t[0] = 'FUNC_CALL', t[1], None

def p_postfix_expression_4(t):
    'postfix_expression : postfix_expression PLUSPLUS'
    t[0] = 'POST_INC', t[1]

def p_postfix_expression_5(t):
    'postfix_expression : postfix_expression MINUSMINUS'
    t[0] = 'POST_DEC', t[1]

# primary-expression:
def p_primary_expression_1(t):
    '''primary_expression : ID'''
    t[0] = 'ID', t[1]

def p_primary_expression_2(t):
    '''primary_expression : constant'''
    t[0] = 'ICONST', t[1]

def p_primary_expression_3(t):
    '''primary_expression : SCONST'''
    t[0] = 'SCONST', t[1]
    # print 'STRING',t[0]
    # print t[1]

def p_primary_expression_4(t):
    '''primary_expression : LPAREN expression RPAREN'''
    t[0] = 'PRIMARY', t[2]

# argument-expression-list:
def p_argument_expression_list_1(t):
    '''argument_expression_list : expression'''
    t[0] = [t[1]]

def p_argument_expression_list_2(t):
    '''argument_expression_list : argument_expression_list COMMA expression'''
    t[0] = t[1] + [t[3]]

# constant:
def p_constant(t): 
   '''constant : ICONST
               | FCONST
               | CCONST'''
   t[0] = t[1]


def p_empty(t):
    'empty : '
    t[0] = None

def p_error(t):
    # print "Whoa, We're hosed"
    if t:
         print("Syntax error at token", t[0])
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")



parser = yacc.yacc(method='LALR')

if __name__ == '__main__':
    s = sys.stdin.read()
    s = remove_blank(remove_comment(s))
    pp.pprint(parser.parse(s))
