#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from itertools import ifilter
from operator import add, sub, neg, mul, div

__author__ = 'mengyu zhang'
__date__ = '10/25/2015'


"""
S   :   E S' 
    |   ε

S'  :   ; S

E   :   T E'

E'  :   [+-] T E'
    |   ε

T   :   F T'

T'  :   [*/] F T'
    |   ε

F   :   const
    |   (E)
"""


def char_stream(s): 
    """
    :param s: input expression.  
    :return: char stream, without space.
    """
    return ifilter(lambda c: not c.isspace(), s)


def token_stream(chars):
    """
    :param chars: char stream, without space.
    :return: token stream, int or symbol + - * / ( ).
    """
    buf = []
    while True:
        c = next(chars, None)
        if c and c.isdigit():
            buf.append(c) 
        else:
            if buf:
                yield int(''.join(buf))
                buf = []
            if c is None:
                break
            yield c


def parse(tokens):
     
    lookahead = list()
    lookahead.append(next(tokens, None))


    def match(t=None):
        if t is not None:
            assert(lookahead[-1] == t)
        lookahead.append(next(tokens, None))


    def sequence():
        if lookahead[-1] is None:
            return []

        exprs = [expr()]
        if lookahead[-1] == ';':
            exprs.extend(sequence_rest())

        return exprs


    def sequence_rest():
        match(';')
        return sequence()


    def expr(): 
        left_op = term()
        return expr_rest(left_op) 


    def expr_rest(left_op): 
        t = lookahead[-1]
        if t in '+-': 
            match(t) 
            if t  == '+': 
                val = left_op + term()
            else: 
                val = left_op - term()
            return expr_rest(val) 
        else: 
            return left_op


    def term(): 
        left_op = factor()
        return term_rest(left_op) 


    def term_rest(left_op): 
        t = lookahead[-1]
        if t in '*/': 
            match(t) 
            if t == '*': 
                val = left_op * factor()
            else: 
                val = left_op / factor()
            return term_rest(val) 
        else: 
            return left_op


    def factor():
        t = lookahead[-1]
        if type(t) == int: 
            match(t)
            return t
        elif t == '(': 
            match('(') 
            val = expr() 
            match(')') 
            return val 
        else: 
            raise ValueError('int or left parenthesis is expected') 

    return sequence()

if __name__ == '__main__': 
    S = raw_input()
    tokens = token_stream(char_stream(S.strip()))

    print parse(tokens)

