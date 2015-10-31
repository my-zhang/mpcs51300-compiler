import sys
import pprint

import clex
import ply.yacc as yacc

pp = pprint.PrettyPrinter(indent=4, width=120)

# token map
tokens = clex.tokens

# symbol table
ST = {}

# translation-unit:

def p_translation_unit_1(t):
    'translation_unit : external_declaration'
    t[0] = [t[1]]
    pp.pprint(t[0])

def p_translation_unit_2(t):
    'translation_unit : translation_unit external_declaration'
    t[0] = t[1] + [t[2]]
    pp.pprint(t[0])

# external-declaration:

def p_external_declaration_1(t):
    '''external_declaration : function_definition
                            | declaration'''
    t[0] = t[1]

def p_external_declaration_2(t):
    'external_declaration : EXTERN declaration'
    t[0] = 'EXTERN', t[2]

# function-definition:
def p_function_definition(t):
    'function_definition : type_specifier declarator compound_statement'
    t[0] = 'FUNC_DEF', t[1], t[2], t[3]

# declaration:
def p_declaration(t):
    'declaration : type_specifier init_declarator_list SEMI'
    t[0] = 'VAR_DEC', t[1], t[2]

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

def p_init_declarator_list_2(t):
    'init_declarator_list : init_declarator_list COMMA init_declarator'
    t[0] = t[1] + [t[3]]

# init-declarator

def p_init_declarator_1(t):
    'init_declarator : declarator'
    t[0] = 'INIT_DEC_1', t[1]

def p_init_declarator_2(t):
    'init_declarator : declarator EQUALS expression'
    t[0] = 'INIT_DEC_2', t[1], t[3]

# struct-declaration:

def p_struct_declaration(t):
    'struct_declaration : specifier_qualifier_list struct_declarator_list SEMI'
    pass

# specifier-qualifier-list:

def p_specifier_qualifier_list_1(t):
    'specifier_qualifier_list : type_specifier specifier_qualifier_list'
    pass

def p_specifier_qualifier_list_2(t):
    'specifier_qualifier_list : type_specifier'
    pass


# struct-declarator-list:

def p_struct_declarator_list_1(t):
    'struct_declarator_list : struct_declarator'
    pass

def p_struct_declarator_list_2(t):
    'struct_declarator_list : struct_declarator_list COMMA struct_declarator'
    pass

# struct-declarator:

def p_struct_declarator_1(t):
    'struct_declarator : declarator'
    pass

def p_struct_declarator_2(t):
    'struct_declarator : declarator COLON constant_expression'
    pass

def p_struct_declarator_3(t):
    'struct_declarator : COLON constant_expression'
    pass

# declarator:

def p_declarator_1(t):
    'declarator : ID'
    t[0] = 'ID', t[1]

def p_declarator_2(t):
    'declarator : ID LPAREN parameter_type_list RPAREN '
    t[0] = t[1], t[3]

def p_declarator_3(t):
    'declarator : ID LPAREN identifier_list RPAREN '
    t[0] = t[1]

def p_declarator_4(t):
    'declarator : ID LPAREN RPAREN '
    t[0] = t[1]

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

# def p_parameter_type_list_2(t):
#     'parameter_type_list : parameter_list COMMA ELLIPSIS'
#     pass

# parameter-list:

def p_parameter_list_1(t):
    'parameter_list : parameter_declaration'
    t[0] = [t[1]]

def p_parameter_list_2(t):
    'parameter_list : parameter_list COMMA parameter_declaration'
    t[0] = t[1] + [t[3]]

# parameter-declaration:
def p_parameter_declaration_1(t):
    'parameter_declaration : type_specifier declarator'
    t[0] = t[1], t[2]

def p_parameter_declaration_2(t):
    'parameter_declaration : type_specifier abstract_declarator_opt'
    pass

# identifier-list:
def p_identifier_list_1(t):
    'identifier_list : ID'
    pass

def p_identifier_list_2(t):
    'identifier_list : identifier_list COMMA ID'
    pass

# type-name:

def p_type_name(t):
    'type_name : specifier_qualifier_list abstract_declarator_opt'
    pass

def p_abstract_declarator_opt_1(t):
    'abstract_declarator_opt : empty'
    pass

def p_abstract_declarator_opt_2(t):
    'abstract_declarator_opt : abstract_declarator'
    pass

# abstract-declarator:

def p_abstract_declarator_1(t):
    'abstract_declarator : pointer '
    pass

def p_abstract_declarator_2(t):
    'abstract_declarator : pointer direct_abstract_declarator'
    pass

def p_abstract_declarator_3(t):
    'abstract_declarator : direct_abstract_declarator'
    pass

# direct-abstract-declarator:

def p_direct_abstract_declarator_1(t):
    'direct_abstract_declarator : LPAREN abstract_declarator RPAREN'
    pass

def p_direct_abstract_declarator_2(t):
    'direct_abstract_declarator : direct_abstract_declarator LBRACKET constant_expression_opt RBRACKET'
    pass

def p_direct_abstract_declarator_3(t):
    'direct_abstract_declarator : LBRACKET constant_expression_opt RBRACKET'
    pass

def p_direct_abstract_declarator_4(t):
    'direct_abstract_declarator : direct_abstract_declarator LPAREN parameter_type_list_opt RPAREN'
    pass

def p_direct_abstract_declarator_5(t):
    'direct_abstract_declarator : LPAREN parameter_type_list_opt RPAREN'
    pass

# Optional fields in abstract declarators

def p_constant_expression_opt_1(t):
    'constant_expression_opt : empty'
    pass

def p_constant_expression_opt_2(t):
    'constant_expression_opt : constant_expression'
    pass

def p_parameter_type_list_opt_1(t):
    'parameter_type_list_opt : empty'
    pass

def p_parameter_type_list_opt_2(t):
    'parameter_type_list_opt : parameter_type_list'
    pass

# statement:

def p_statement(t):
    '''
    statement : labeled_statement
              | expression_statement
              | compound_statement
              | selection_statement
              | iteration_statement
              | jump_statement
              '''
    t[0] = 'STAT', t[1]

# labeled-statement:

def p_labeled_statement_1(t):
    'labeled_statement : ID COLON statement'
    pass

def p_labeled_statement_2(t):
    'labeled_statement : CASE constant_expression COLON statement'
    pass

def p_labeled_statement_3(t):
    'labeled_statement : DEFAULT COLON statement'
    pass

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
    'selection_statement : IF LPAREN expression RPAREN statement'
    t[0] = 'IF', t[3], t[5]

def p_selection_statement_2(t):
    'selection_statement : IF LPAREN expression RPAREN statement ELSE statement '
    t[0] = 'IF_ELSE', t[3], t[5], t[7]

# iteration_statement:
def p_iteration_statement_1(t):
    'iteration_statement : WHILE LPAREN expression RPAREN statement'
    pass

def p_iteration_statement_2(t):
    'iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement '
    t[0] = 'ITER_STAT_2', t[3], t[5], t[7], t[9]

def p_iteration_statement_3(t):
    'iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI'
    pass

# jump_statement:
def p_jump_statement(t):
    'jump_statement : RETURN expression_opt SEMI'
    t[0] = 'RET', t[2]

def p_expression_opt_1(t):
    'expression_opt : empty'
    t[0] = t[1]

def p_expression_opt_2(t):
    'expression_opt : expression'
    t[0] = t[1]

# expression:

def p_expression_1(t):
    'expression : equality_expression'
    t[0] = 'EXPR_1', t[1]

def p_expression_2(t):
    'expression : unary_expression assignment_operator expression'
    t[0] = 'EXPR_2', t[1], t[2], t[3]

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


# constant-expression
def p_constant_expression(t):
    'constant_expression : equality_expression'
    t[0] = t[1]

# equality-expression:
def p_equality_expression_1(t):
    'equality_expression : relational_expression'
    t[0] = t[1]

def p_equality_expression_2(t):
    'equality_expression : equality_expression EQ relational_expression'
    pass

def p_equality_expression_3(t):
    'equality_expression : equality_expression NE relational_expression'
    pass


# relational-expression:
def p_relational_expression_1(t):
    'relational_expression : additive_expression'
    t[0] = t[1]

def p_relational_expression_2(t):
    'relational_expression : relational_expression LT additive_expression'
    t[0] = t[1], t[2], t[3]

def p_relational_expression_3(t):
    'relational_expression : relational_expression GT additive_expression'
    t[0] = t[1], t[2], t[3]

def p_relational_expression_4(t):
    'relational_expression : relational_expression LE additive_expression'
    t[0] = t[1], t[2], t[3]

def p_relational_expression_5(t):
    'relational_expression : relational_expression GE additive_expression'
    t[0] = t[1], t[2], t[3]


# additive-expression

def p_additive_expression_1(t):
    'additive_expression : multiplicative_expression'
    t[0] = t[1]

def p_additive_expression_2(t):
    'additive_expression : additive_expression PLUS multiplicative_expression'
    t[0] = t[1], t[2], t[3]

def p_additive_expression_3(t):
    'additive_expression : additive_expression MINUS multiplicative_expression'
    pass

# multiplicative-expression

def p_multiplicative_expression_1(t):
    'multiplicative_expression : unary_expression'
    t[0] = t[1]

def p_multiplicative_expression_2(t):
    'multiplicative_expression : multiplicative_expression TIMES unary_expression'
    pass

def p_multiplicative_expression_3(t):
    'multiplicative_expression : multiplicative_expression DIVIDE unary_expression'
    pass

def p_multiplicative_expression_4(t):
    'multiplicative_expression : multiplicative_expression MOD unary_expression'
    pass


# unary-expression:
def p_unary_expression_1(t):
    'unary_expression : postfix_expression'
    t[0] = t[1]

def p_unary_expression_2(t):
    'unary_expression : unary_operator unary_expression'
    t[0] = t[1], t[2]

#unary-operator
def p_unary_operator(t):
    '''unary_operator : AND
                      | TIMES
                      | PLUS 
                      | MINUS
                      | NOT
                      | LNOT '''
    t[0] = t[1]


# postfix-expression:

def p_postfix_expression_1(t):
    'postfix_expression : primary_expression'
    t[0] = t[1]

def p_postfix_expression_2(t):
    'postfix_expression : postfix_expression LBRACKET expression RBRACKET'
    pass

def p_postfix_expression_3(t):
    'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
    t[0] = 'POST_FUNC_CALL', t[1], t[3]

def p_postfix_expression_4(t):
    'postfix_expression : postfix_expression LPAREN RPAREN'
    t[0] = 'POST_FUNC_CALL', t[1]

def p_postfix_expression_5(t):
    'postfix_expression : postfix_expression PLUSPLUS'
    t[0] = 'POST_INC', t[1], t[2]

def p_postfix_expression_6(t):
    'postfix_expression : postfix_expression MINUSMINUS'
    t[0] = 'POST_DEC', t[1], t[2]

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
    print "Whoa. We're hosed"


parser = yacc.yacc(method='LALR')

if __name__ == '__main__':
    s = sys.stdin.read()
    parser.parse(s)
