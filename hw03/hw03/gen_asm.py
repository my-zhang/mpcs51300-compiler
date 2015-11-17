import sys
from functools import partial

import ply.yacc as yacc
import cparse

instructions = []
st = []

def is_sth(root, t):
    return root[0] in t

is_func_def             = partial(is_sth, t=['FUNC_DEF'])
is_declaration          = partial(is_sth, t=['VAR_DEC'])
is_instruction          = partial(is_sth, t=['STAT'])
is_init_assign          = partial(is_sth, t=['INIT_ASSIGN'])
is_additive_expr        = partial(is_sth, t=['ADD', 'SUB'])
is_multiplicative_expr  = partial(is_sth, t=['MUL', 'DIV'])
is_iconst               = partial(is_sth, t=['ICONST'])
is_id                   = partial(is_sth, t=['ID'])

def add_asm(s):
    instructions.append(s)

def add_op_asm(op):
    add_asm('popq %rbx') 
    add_asm('popq %rax') 
    add_asm('altd') 
    add_asm('%s %%rbx, %%rax' %(op)) 
    add_asm('pushq %rax') 

def traverse_ast(root):
    if is_func_def(root):
        _, t, f, insts = root
        traverse_compound_instruction(insts)

def traverse_compound_instruction(insts):
    _, lst = insts
    declaration_list = filter(is_declaration, lst)
    instruction_list = filter(is_instruction, lst)

    map(traverse_delaration, declaration_list)
    map(traverse_instruction, instruction_list)

def traverse_delaration(dec):
    _, t, lst = dec
    map(traverse_var_declarator, lst)

def traverse_instruction(inst):
    pass

def traverse_var_declarator(declarator):
    if is_init_assign(declarator):
        _, (_, x), v = declarator
        traverse_expression(v)
    else:
        _, (_, x) = declarator

def traverse_expression(expr):
    if is_iconst(expr):
        _, n = expr
        add_asm('pushq $%s' %(n))

    elif is_additive_expr(expr):
        op, a, b = expr
        traverse_expression(a)
        traverse_expression(b)
        add_op_asm('addq' if op == 'ADD' else 'subq')

    elif is_multiplicative_expr(expr):
        op, a, b = expr
        traverse_expression(a)
        traverse_expression(b)
        add_op_asm('imulq' if op == 'MUL' else 'idivq')

if __name__ == '__main__':
    parser = cparse.parser
    asts = parser.parse(sys.stdin.read())
    map(traverse_ast, asts)
    print '\n'.join(instructions)
