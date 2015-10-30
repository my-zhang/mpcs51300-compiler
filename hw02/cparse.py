# -----------------------------------------------------------------------------
# cparse.py
#
# Simple parser for ANSI C.  Based on the grammar in K&R, 2nd Ed.
# -----------------------------------------------------------------------------

import sys
import pprint

import clex
import ply.yacc as yacc

pp = pprint.PrettyPrinter(indent=4)

# Get the token map
tokens = clex.tokens

# Symbol Table
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
    'external_declaration : function_definition'
    t[0] = 'FUNC_DEF', t[1]

def p_external_declaration_2(t):
    'external_declaration : declaration'
    t[0] = 'VARS_DEC', t[1]

# function-definition:

def p_function_definition_1(t):
    'function_definition : declaration_specifiers declarator declaration_list compound_statement'
    t[0] = 'FUNC_DEF_1', t[1], t[2], t[3], t[4]

def p_function_definition_2(t):
    'function_definition : declarator declaration_list compound_statement'
    t[0] = 'FUNC_DEF_2', t[1], t[2], t[3]

def p_function_definition_3(t):
    'function_definition : declarator compound_statement'
    t[0] = 'FUNC_DEF_3', t[1], t[2]

def p_function_definition_4(t):
    'function_definition : declaration_specifiers declarator compound_statement'
    t[0] = 'FUNC_DEF_4', t[1], t[2], t[3]

# declaration:

def p_declaration_1(t):
    'declaration : declaration_specifiers init_declarator_list SEMI'
    t[0] = 'VAR_DEC', t[0], t[2]

def p_declaration_2(t):
    'declaration : declaration_specifiers SEMI'
    t[0] = t[1]

# declaration-list:

def p_declaration_list_1(t):
    'declaration_list : declaration'
    t[0] = [t[1]]

def p_declaration_list_2(t):
    'declaration_list : declaration_list declaration '
    t[0] = t[1] + [t[2]]

# declaration-specifiers
def p_declaration_specifiers_1(t):
    'declaration_specifiers : storage_class_specifier declaration_specifiers'
    t[0] = t[1], t[2]

def p_declaration_specifiers_2(t):
    'declaration_specifiers : type_specifier declaration_specifiers'
    t[0] = t[1], t[2]


def p_declaration_specifiers_3(t):
    'declaration_specifiers : storage_class_specifier'
    t[0] = t[1]

def p_declaration_specifiers_4(t):
    'declaration_specifiers : type_specifier'
    t[0] = t[1]


# storage-class-specifier
def p_storage_class_specifier(t):
    '''storage_class_specifier : AUTO
                               | REGISTER
                               | STATIC
                               | EXTERN
                               | TYPEDEF
                               '''
    pass

# type-specifier:
def p_type_specifier(t):
    '''type_specifier : VOID
                      | CHAR
                      | SHORT
                      | INT
                      | LONG
                      | FLOAT
                      | DOUBLE
                      | SIGNED
                      | UNSIGNED
                      | struct_or_union_specifier
                      | enum_specifier
                      | TYPEID
                      '''
    t[0] = t[1]


# struct-or-union-specifier

def p_struct_or_union_specifier_1(t):
    'struct_or_union_specifier : struct_or_union ID LBRACE struct_declaration_list RBRACE'
    pass

def p_struct_or_union_specifier_2(t):
    'struct_or_union_specifier : struct_or_union LBRACE struct_declaration_list RBRACE'
    pass

def p_struct_or_union_specifier_3(t):
    'struct_or_union_specifier : struct_or_union ID'
    pass

# struct-or-union:
def p_struct_or_union(t):
    '''struct_or_union : STRUCT
                       | UNION
                       '''
    pass

# struct-declaration-list:

def p_struct_declaration_list_1(t):
    'struct_declaration_list : struct_declaration'
    pass

def p_struct_declaration_list_2(t):
    'struct_declaration_list : struct_declarator_list struct_declaration'
    pass

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
    'init_declarator : declarator EQUALS initializer'
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

# enum-specifier:

def p_enum_specifier_1(t):
    'enum_specifier : ENUM ID LBRACE enumerator_list RBRACE'
    pass

def p_enum_specifier_2(t):
    'enum_specifier : ENUM LBRACE enumerator_list RBRACE'
    pass

def p_enum_specifier_3(t):
    'enum_specifier : ENUM ID'
    pass

# enumerator_list:
def p_enumerator_list_1(t):
    'enumerator_list : enumerator'
    pass

def p_enumerator_list_2(t):
    'enumerator_list : enumerator_list COMMA enumerator'
    pass

# enumerator:
def p_enumerator_1(t):
    'enumerator : ID'
    pass

def p_enumerator_2(t):
    'enumerator : ID EQUALS constant_expression'
    pass

# declarator:

def p_declarator_1(t):
    'declarator : pointer direct_declarator'
    pass

def p_declarator_2(t):
    'declarator : direct_declarator'
    t[0] = t[1]
    # print t[0]

# direct-declarator:

def p_direct_declarator_1(t):
    'direct_declarator : ID'
    t[0] = t[1]

def p_direct_declarator_2(t):
    'direct_declarator : LPAREN declarator RPAREN'
    pass

def p_direct_declarator_3(t):
    'direct_declarator : direct_declarator LBRACKET constant_expression_opt RBRACKET'
    pass

def p_direct_declarator_4(t):
    'direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN '
    t[0] = (t[1], t[3])

def p_direct_declarator_5(t):
    'direct_declarator : direct_declarator LPAREN identifier_list RPAREN '
    t[0] = t[1]

def p_direct_declarator_6(t):
    'direct_declarator : direct_declarator LPAREN RPAREN '
    pass

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
    'parameter_declaration : declaration_specifiers declarator'
    t[0] = t[1], t[2]

def p_parameter_declaration_2(t):
    'parameter_declaration : declaration_specifiers abstract_declarator_opt'
    pass

# identifier-list:
def p_identifier_list_1(t):
    'identifier_list : ID'
    pass

def p_identifier_list_2(t):
    'identifier_list : identifier_list COMMA ID'
    pass

# initializer:

def p_initializer_1(t):
    'initializer : assignment_expression'
    pass

def p_initializer_2(t):
    '''initializer : LBRACE initializer_list RBRACE
                   | LBRACE initializer_list COMMA RBRACE'''
    pass

# initializer-list:

def p_initializer_list_1(t):
    'initializer_list : initializer'
    pass

def p_initializer_list_2(t):
    'initializer_list : initializer_list COMMA initializer'
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
    pass

# compound-statement:

def p_compound_statement_1(t):
    'compound_statement : LBRACE declaration_list statement_list RBRACE'
    t[0] = 'COMP_STATS_1', t[2] + t[3]

def p_compound_statement_2(t):
    'compound_statement : LBRACE statement_list RBRACE'
    t[0] = 'COMP_STATS_2', t[2]

def p_compound_statement_3(t):
    'compound_statement : LBRACE declaration_list RBRACE'
    t[0] = 'COMP_STATS_3', t[2] 

def p_compound_statement_4(t):
    'compound_statement : LBRACE RBRACE'
    t[0] = 'COMP_STATS_4', []

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
    pass

def p_selection_statement_2(t):
    'selection_statement : IF LPAREN expression RPAREN statement ELSE statement '
    pass

def p_selection_statement_3(t):
    'selection_statement : SWITCH LPAREN expression RPAREN statement '
    pass

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

def p_jump_statement_1(t):
    'jump_statement : GOTO ID SEMI'
    pass

def p_jump_statement_2(t):
    'jump_statement : CONTINUE SEMI'
    pass

def p_jump_statement_3(t):
    'jump_statement : BREAK SEMI'
    pass

def p_jump_statement_4(t):
    'jump_statement : RETURN expression_opt SEMI'
    pass

def p_expression_opt_1(t):
    'expression_opt : empty'
    t[0] = t[1]

def p_expression_opt_2(t):
    'expression_opt : expression'
    t[0] = t[1]

# expression:
def p_expression(t):
    'expression : assignment_expression'
    t[0] = t[1]

# assigment_expression:
def p_assignment_expression_1(t):
    'assignment_expression : conditional_expression'
    t[0] = t[1]

def p_assignment_expression_2(t):
    'assignment_expression : unary_expression assignment_operator assignment_expression'
    t[0] = t[1], t[2], t[3]

# assignment_operator:
def p_assignment_operator(t):
    '''
    assignment_operator : EQUALS
                        | TIMESEQUAL
                        | DIVEQUAL
                        | MODEQUAL
                        | PLUSEQUAL
                        | MINUSEQUAL
                        | LSHIFTEQUAL
                        | RSHIFTEQUAL
                        | ANDEQUAL
                        | OREQUAL
                        | XOREQUAL
                        '''
    t[0] = t[1]

# conditional-expression
def p_conditional_expression_1(t):
    'conditional_expression : equality_expression'
    pass

def p_conditional_expression_2(t):
    'conditional_expression : equality_expression CONDOP expression COLON conditional_expression '
    pass

# constant-expression

def p_constant_expression(t):
    'constant_expression : conditional_expression'
    pass

# equality-expression:

def p_equality_expression_1(t):
    'equality_expression : relational_expression'
    pass

def p_equality_expression_2(t):
    'equality_expression : equality_expression EQ relational_expression'
    pass

def p_equality_expression_3(t):
    'equality_expression : equality_expression NE relational_expression'
    pass


# relational-expression:
def p_relational_expression_1(t):
    'relational_expression : additive_expression'
    pass

def p_relational_expression_2(t):
    'relational_expression : relational_expression LT additive_expression'
    pass

def p_relational_expression_3(t):
    'relational_expression : relational_expression GT additive_expression'
    pass

def p_relational_expression_4(t):
    'relational_expression : relational_expression LE additive_expression'
    pass

def p_relational_expression_5(t):
    'relational_expression : relational_expression GE additive_expression'
    pass


# additive-expression

def p_additive_expression_1(t):
    'additive_expression : multiplicative_expression'
    pass

def p_additive_expression_2(t):
    'additive_expression : additive_expression PLUS multiplicative_expression'
    pass

def p_additive_expression_3(t):
    'additive_expression : additive_expression MINUS multiplicative_expression'
    pass

# multiplicative-expression

def p_multiplicative_expression_1(t):
    'multiplicative_expression : unary_expression'
    pass

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
    pass

def p_postfix_expression_4(t):
    'postfix_expression : postfix_expression LPAREN RPAREN'
    pass

def p_postfix_expression_5(t):
    'postfix_expression : postfix_expression PLUSPLUS'
    t[0] = t[1], t[2]

def p_postfix_expression_6(t):
    'postfix_expression : postfix_expression MINUSMINUS'
    pass

# primary-expression:
def p_primary_expression_1(t):
    '''primary_expression : ID
                          | constant
                          | SCONST'''
    t[0] = t[1]

def p_primary_expression_2(t):
    '''primary_expression : LPAREN expression RPAREN'''
    t[0] = t[2]

# argument-expression-list:
def p_argument_expression_list(t):
    '''argument_expression_list :  assignment_expression
                              |  argument_expression_list COMMA assignment_expression'''
    pass

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

