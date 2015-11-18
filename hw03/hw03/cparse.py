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

def p_external_declaration_2(t):
    '''external_declaration : declaration'''
    t[0] = t[1]

def p_external_declaration_3(t):
    'external_declaration : EXTERN declaration'
    t[0] = 'EXTERN', t[2]

# function-definition:
def p_function_definition(t):
    'function_definition : type function_declarator compound_instruction'
    t[0] = 'FUNC_DEF', t[1], t[2], t[3]

# declaration:
def p_declaration(t):
    'declaration : type declarator_list SEMI'
    t[0] = 'VAR_DEC', t[1], t[2]

# declaration-list:
def p_declaration_list_1(t):
    'declaration_list : declaration'
    t[0] = [t[1]]

def p_declaration_list_2(t):
    'declaration_list : declaration_list declaration '
    t[0] = t[1] + [t[2]]


# type-specifier:
def p_type(t):
    '''type : INT
            | FLOAT
            | STRING
                      '''
    t[0] = 'TYPE', t[1]

# init-declarator-list:

def p_declarator_list_1(t):
    'declarator_list : declarator'
    t[0] = [t[1]]

def p_declarator_list_2(t):
    'declarator_list : declarator_list COMMA declarator'
    t[0] = t[1] + [t[3]]

# init-declarator

def p_declarator_1(t):
    'declarator : function_declarator'
    t[0] = t[1]

def p_declarator_2(t):
    'declarator : function_declarator EQUALS expression'
    t[0] = 'INIT_ASSIGN', t[1], t[3]

# declarator:

def p_function_declarator_1(t):
    'function_declarator : ID'
    t[0] = 'ID', t[1]

def p_function_declarator_2(t):
    'function_declarator : ID LPAREN parameter_list RPAREN '
    t[0] = ('ID', t[1]), t[3]

def p_function_declarator_3(t):
    'function_declarator : ID LPAREN RPAREN '
    t[0] = ('ID', t[1]), None

def p_parameter_list_1(t):
    'parameter_list : parameter_declaration'
    t[0] = [t[1]]

def p_parameter_list_2(t):
    'parameter_list : parameter_list COMMA parameter_declaration'
    t[0] = t[1] + [t[3]]

# parameter-declaration:
def p_parameter_declaration(t):
    'parameter_declaration : type function_declarator'
    t[0] = t[1], t[2]

# instruction:

def p_instruction(t):
    '''
    instruction : expression_instruction
              | compound_instruction
              | select_instruction
              | iteration_instruction
              | jump_instruction
              '''
    t[0] = 'STAT', t[1]

# expression-instruction:
def p_expression_instruction(t):
    'expression_instruction : expression SEMI'
    t[0] = t[1]

# compound-instruction:

def p_compound_instruction_1(t):
    'compound_instruction : LBRACE declaration_list instruction_list RBRACE'
    t[0] = 'COMP_STATS', t[2] + t[3]

def p_compound_instruction_2(t):
    'compound_instruction : LBRACE instruction_list RBRACE'
    t[0] = 'COMP_STATS', t[2]

def p_compound_instruction_3(t):
    'compound_instruction : LBRACE declaration_list RBRACE'
    t[0] = 'COMP_STATS', t[2] 

def p_compound_instruction_4(t):
    'compound_instruction : LBRACE RBRACE'
    t[0] = 'COMP_STATS', []

# instruction-list:

def p_instruction_list_1(t):
    'instruction_list : instruction'
    t[0] = [t[1]]

def p_instruction_list_2(t):
    'instruction_list : instruction_list instruction'
    t[0] = t[1] + [t[2]]

# selection-instruction

def p_select_instruction_1(t):
    'select_instruction : IF LPAREN condition RPAREN instruction'
    t[0] = 'IF', t[3], t[5]

def p_select_instruction_2(t):
    'select_instruction : IF LPAREN condition RPAREN instruction ELSE instruction '
    t[0] = 'IF_ELSE', t[3], t[5], t[7]

# iteration_instruction:
def p_iteration_instruction_1(t):
    'iteration_instruction : WHILE LPAREN condition RPAREN instruction'
    t[0] = 'WHILE', t[3], t[5]

def p_iteration_instruction_2(t):
    'iteration_instruction : FOR LPAREN expression SEMI condition SEMI expression RPAREN instruction '
    t[0] = 'FOR', t[3], t[5], t[7], t[9]

def p_iteration_instruction_3(t):
    'iteration_instruction : DO instruction WHILE LPAREN condition RPAREN SEMI'
    t[0] = 'DO_WHILE', t[2], t[5]

# jump_instruction:
def p_jump_instruction(t):
    'jump_instruction : RETURN expression SEMI'
    t[0] = 'RET', t[2]

# expression:

def p_expression_1(t):
    'expression : additive_expression'
    t[0] = t[1]

def p_expression_2(t):
    'expression : unary_expression assignment_operator expression'
    t[0] = 'ASSIGN', t[1], t[3]

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
    t[0] = t[1]

def p_primary_expression_3(t):
    '''primary_expression : SCONST'''
    t[0] = 'SCONST', t[1]

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
   '''constant : ICONST'''
   t[0] = 'ICONST',t[1]

def p_constant_1(t):
    '''constant : FCONST'''
    t[0] = 'FCONST',t[1]

def p_error(t):
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
