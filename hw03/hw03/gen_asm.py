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
is_ret_instruction      = partial(is_sth, t=['RET'])
is_expr_instruction     = partial(is_sth, t=['ASSIGN', 'FUNC_CALL'])
is_assign_instruction   = partial(is_sth, t=['ASSIGN'])
is_func_call            = partial(is_sth, t=['FUNC_CALL'])

def add_asm(s):
    instructions.append(s)

def add_op_asm(op):
    add_asm('popq %rbx') 
    add_asm('popq %rax') 
    add_asm('cltd') 
    add_asm('%s %%rbx, %%rax' %(op)) 
    add_asm('pushq %rax') 

def add_func_dec_asm(fn):
    add_asm('.globl _%s' %(fn))
    add_asm('_%s:' %(fn))
    add_asm('pushq %rbp')
    add_asm('movq %rsp, %rbp')
    add_asm('subq $256, %rsp')

def add_ret_asm():
    add_asm('popq %rax')
    add_asm('addq $256, %rsp')
    add_asm('popq %rbp')
    add_asm('retq')

def enter_block(blk_name):
    st.append({'syms':{}, 'name': blk_name})

def leave_block():
    st.pop()

def find_sym(s):
    for table in st[::-1]:
        if s in table['syms']:
            return table['syms'][s]
    raise ValueError("Can't find symbol %s." %(s))

def insert_sym(s):
    table = st[-1]
    if s in table:
        raise ValueError("%s conflict in block %s." %(s, table['name']))
    table['syms'][s] = len(table['syms'])

def addr_of_sym(x):
    idx = find_sym(x)
    return '-%d(%%rbp)' %(8 * (idx+1))

def reg_of_arg(idx):
    return 'r%d' %(idx + 8)

def traverse_ast(root):
    if is_func_def(root):
        _, t, f, insts = root
        traverse_func_declarator(f)
        traverse_compound_instruction(insts)
        leave_block()

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
    if is_ret_instruction(inst[1]):
        # RET
        _, v = inst[1]
        traverse_expression(v)
        add_ret_asm()

    elif is_assign_instruction(inst[1]):
        _, (_, x), v = inst[1]
        traverse_expression(v)
        add_asm('popq %s' %(addr_of_sym(x)))

    elif is_expr_instruction(inst[1]):
        traverse_expression(inst[1])

    
def traverse_var_declarator(declarator):
    if is_init_assign(declarator):
        # _, (_, x), v = declarator
        # traverse_expression(v)
        pass
    else:
        _, x = declarator
        insert_sym(x)

def traverse_func_declarator(declarator):
    (_, fn), params = declarator
    enter_block(fn)
    add_func_dec_asm(fn)
    if params:
        for i, (t, (_, x)) in enumerate(params):
            insert_sym(x)
            add_asm('movq %%%s, %s' %(reg_of_arg(i), addr_of_sym(x)))

def traverse_expression(expr):
    if is_iconst(expr):
        _, n = expr
        add_asm('pushq $%s' %(n))

    if is_id(expr):
        _, x = expr
        add_asm('pushq %s' %(addr_of_sym(x)))

    elif is_func_call(expr):
        _, (_, f), args = expr

        for i, expr in enumerate(args):
            traverse_expression(expr)
            add_asm('popq %%%s' %(reg_of_arg(i)))

        add_asm('call _%s' %(f))
        add_asm('pushq %rax')

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

    enter_block('global')
    map(traverse_ast, asts)
    leave_block()

    print '\n'.join(instructions)
