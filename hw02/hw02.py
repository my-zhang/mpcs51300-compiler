import sys
import pprint

import ply.yacc as yacc
import cparse

from uuid import uuid4

pp = pprint.PrettyPrinter(indent=4, width=120)

parser = cparse.parser

def insert_sym(syms, st, s, val):
    if s not in syms:
        syms[s] = {}

    key = '$'.join(map(str, st)) if st else 'global'

    if key in syms[s]:
        raise ValueError('symbols conflit. %s %s' %(key, str(sym[s][key])))

    syms[s][key] = val

    return syms

def print_syms(syms):
    for s, d in syms.items():
        print s,
        for scope, val in d.items():
            print '\t%-20s %-20s' %(str(val), scope)

def parse_func_dec(root, st, syms):
    cons, type_specifier, declarator, compound_statement = root
    (_, f), params = declarator

    insert_sym(syms, st, f, ('FUNC', type_specifier[1]))

    st.append(f)
    parse_param_list(params, st, syms)
    parse_compound_statement(compound_statement, st, syms)
    st.pop()


def parse_var_dec(root, st, syms):
    cons, (_, t), init_declarator_list = root 
    
    for init_dec in init_declarator_list:
        if init_dec[0] == 'ID':
            _, d = init_dec
        elif init_dec[0] == 'INIT_ASSIGN':
            _, (_, d), expr = init_dec
        else:
            (_, d), params = init_dec
            st.append(d)
            parse_param_list(params, st, syms)
            st.pop()
        
        insert_sym(syms, st, d, t)


def parse_param_list(root, st, syms):
    def parse_param(param, st, syms):
        (_, t), (_, d) = param
        insert_sym(syms, st, d, t)

    for p in root:
        parse_param(p, st, syms)

def parse_compound_statement(root, st, syms):
    cons, comp_list = root

    for comp_stat in comp_list:
        if comp_stat[0] == 'STAT':
            parse_statement(comp_stat, st, syms)
        elif comp_stat[0] == 'VAR_DEC':
            parse_var_dec(comp_stat, st, syms)
        else:
            pass

def parse_statement(root, st, syms):
    _, stat = root
    if stat[0] == 'FOR':
        _, init_assign, condition, post_assign, statement = stat
        st.append('for_%s' %str(uuid4()))
        parse_statement(statement, st, syms)
        st.pop()
    elif stat[0] == 'COMP_STATS':
        parse_compound_statement(stat, st, syms)
    elif stat[0] == 'ASSIGN':
        pass
    else:
        pass
    
if __name__ == '__main__':
    ast = parser.parse(sys.stdin.read())
    pp.pprint(ast)

    st = []
    syms = {}

    for blk in ast:
        if blk[0] == 'FUNC_DEF':
            parse_func_dec(blk, st, syms)
        elif blk[0] == 'VAR_DEC':
            parse_var_dec(blk, st, syms)
        elif blk[0] == 'EXTERN':
            st.append('extern')
            parse_var_dec(blk[1], st, syms)
            st.pop()
        else:
            pass

    print_syms(syms)
