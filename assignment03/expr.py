#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ply.lex as lex
import ply.yacc as yacc

__author__ = 'mengyu zhang'
__date__ = '10/25/2015'

tokens = ('NUMBER','ADD','MUL','LPAREN','RPAREN')

t_ADD    = r'\+'
t_MUL   = r'\*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    

def t_error(t):
    print 'Unexpected Token', t
    t.lexer.skip(1)
    
lexer = lex.lex()

precedence = ('left','ADD'), ('left','MUL')


def p_expression_term(t):
    '''
    expression : expression ADD term
               | term
    '''
    if(len(t) > 2):
      t[0] = t[1] + t[3]
    else:
      t[0] = t[1]


def p_term_factor(t):
    '''
    term : term MUL factor
         | factor
    '''
    if(len(t)>2):
      t[0] = t[1] * t[3]
    else:
      t[0] = t[1]


def p_factor_group(t):
    '''
    factor : LPAREN expression RPAREN
    '''
    t[0] = t[2]


def p_factor_number(t):
    '''
    factor : NUMBER
    '''
    t[0] = t[1]


def p_error(t):
    print 'Parsing Error'


parser = yacc.yacc()

if __name__ == '__main__':
   S = raw_input()
   print(parser.parse(S))
