#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ply.lex as lex
import ply.yacc as yacc

__author__ = 'mengyu zhang'
__date__ = '11/01/2015'

tokens = ('NUMBER', 'ADD', 'MUL', 'SUB', 'DIV', 
            'LPAREN', 'RPAREN', 'SEMI', 'ASSIGN', 'NAME')

t_ADD       = r'\+'
t_SUB       = r'-'
t_MUL       = r'\*'
t_DIV       = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_SEMI      = r';'
t_ASSIGN    = r':='

t_ignore    = " \t"

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_error(t):
    print 'Unexpected Token', t
    t.lexer.skip(1)
    
lexer = lex.lex()

precedence = ('left','ADD'), ('left','MUL')

D = {}


def p_statement_1(t):
    '''
    statement : instruction SEMI statement
    '''
    t[0] = [t[1]] + t[3]
    
def p_statement_2(t):
    '''
    statement : epsilon
    '''
    t[0] = []

def p_instruction_1(t):
    '''
    instruction : NAME ASSIGN expression
    '''
    D[t[1]] = t[3]
    t[0] = None
    print 'pop', t[1]

def p_instruction_2(t):
    '''
    instruction : expression
    '''
    t[0] = t[1]
    print 'pop', 'output'

def p_instruction_3(t):
    '''
    instruction : epsilon
    '''
    t[0] = None

def p_expression_1(t):
    '''
    expression : expression ADD term
    '''
    t[0] = t[1] + t[3]
    print 'add'

def p_expression_2(t):
    '''
    expression : expression SUB term
    '''
    t[0] = t[1] - t[3]
    print 'sub'

def p_expression_3(t):
    '''
    expression : term
    '''
    t[0] = t[1]

def p_term_1(t):
    '''
    term : term MUL factor
    '''
    t[0] = t[1] * t[3]
    print 'mul'

def p_term_2(t):
    '''
    term : term DIV factor
    '''
    t[0] = t[1] / t[3]
    print 'div'

def p_term_3(t):
    '''
    term : factor
    '''
    t[0] = t[1]

def p_factor_1(t):
    '''
    factor : LPAREN expression RPAREN
    '''
    t[0] = t[2]


def p_factor_2(t):
    '''
    factor : NUMBER
    '''
    t[0] = t[1]
    print 'push', t[1]

def p_factor_3(t):
    '''
    factor : NAME
    '''
    if t[1] not in D:
        raise ValueError("symbol %s is not defined." %(t[1]))
    t[0] = D[t[1]]
    print 'push', t[1]

def p_epsilon(t):
    'epsilon : '
    pass

def p_error(t):
    print 'Parsing Error'


parser = yacc.yacc()

if __name__ == '__main__':
   S = raw_input()
   print(parser.parse(S))
