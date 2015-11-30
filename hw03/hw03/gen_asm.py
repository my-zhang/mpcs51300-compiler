import sys
from uuid import uuid4
from functools import partial

import ply.yacc as yacc
import cparse

from preprocess import remove_blank
from preprocess import remove_comment

instructions = []
st = []
num_string = 0
call_cat = False
exist_str = False
string_ins = []

def gen_id():
    return '_'.join(str(uuid4()).split('-'))

def is_sth(root, t):
    return root[0] in t

is_func_def             = partial(is_sth, t=['FUNC_DEF'])
is_declaration          = partial(is_sth, t=['VAR_DEC'])
is_instruction          = partial(is_sth, t=['STAT'])
is_init_assign          = partial(is_sth, t=['INIT_ASSIGN'])
is_shift_expr           = partial(is_sth, t=['LSHIFT', 'RSHIFT'])
is_additive_expr        = partial(is_sth, t=['ADD', 'SUB'])
is_multiplicative_expr  = partial(is_sth, t=['MUL', 'DIV', 'MOD'])
is_neg_expr             = partial(is_sth, t=['NEG'])
is_primary_expr         = partial(is_sth, t=['PRIMARY'])
is_iconst               = partial(is_sth, t=['ICONST'])
is_sconst               = partial(is_sth, t=['SCONST'])
is_id                   = partial(is_sth, t=['ID'])
is_ret_instruction      = partial(is_sth, t=['RET'])
is_expr_instruction     = partial(is_sth, t=['ASSIGN', 'FUNC_CALL'])
is_assign_instruction   = partial(is_sth, t=['ASSIGN'])
is_select_instruction   = partial(is_sth, t=['IF', 'IF_ELSE'])
is_compound_instruction = partial(is_sth, t=['COMP_STATS'])
is_iter_instruction     = partial(is_sth, t=['WHILE', 'FOR', 'DO_WHILE'])
is_func_call            = partial(is_sth, t=['FUNC_CALL'])

op_to_cmd = {'<':   'jge',
             '<=':  'jg',
             '>':   'jle',
             '>=':  'jl',
             '==':  'jne',
             '!=':  'je'}

def add_asm(s):
    instructions.append(s)

def add_op_asm(op):
    add_asm('popq %rbx') 
    add_asm('popq %rax') 
    add_asm('cltd') 
    add_asm('cqo') 
    add_asm('%s %%rbx, %%rax' %(op)) 
    add_asm('pushq %rax') 

def add_cmp_asm(op):
    add_asm('popq %rbx') 
    add_asm('popq %rax') 
    add_asm('cmpq %rbx, %rax') 

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

def add_str_literal_asm():
    # add_asm('.section __TEXT,__cstring,cstring_literals')
    add_asm('L_.str:')
    add_asm('.asciz "%d\\n"')

def enter_block(blk_name, t='func'):
    if t == 'func':
        st.append({'syms': {}, 'name': blk_name, 'env': {'count': 0}})
    elif t == 'local':
        st.append({'syms': {}, 'name': blk_name, 'env': st[-1]['env']})
    else:
        raise ValueError('Unknown scope name %s.' %t)

def if_exist_string():
    global exist_str
    if(exist_str):
        for single_ins in string_ins:
            add_asm(single_ins)
def if_call_cat():
    global call_cat
    if(call_cat):
        add_asm('_cat:')        
        add_asm('pushq %rbp')
        add_asm('movq    %rsp, %rbp')
        add_asm('subq    $64, %rsp')
        add_asm('movl    $128, %eax')
        add_asm('movl    %eax, %ecx')
        add_asm('movq    %rdi, -8(%rbp)')
        add_asm('movq    %rsi, -16(%rbp)')
        add_asm('movq    %rcx, %rdi')
        add_asm('callq   _malloc')
        add_asm('movl    $127, %edx')
        add_asm('movq    %rax, -24(%rbp)')
        add_asm('movq    -24(%rbp), %rdi')
        add_asm('movq    -8(%rbp), %rsi')
        add_asm('callq   _strncpy')
        add_asm('movl    $127, %r8d')
        add_asm('movl    %r8d, %ecx')
        add_asm('movq    -24(%rbp), %rdi')
        add_asm('movq    -16(%rbp), %rsi')
        add_asm('movq    -24(%rbp), %rdx')
        add_asm('movq    %rdi, -32(%rbp)')       
        add_asm('movq    %rdx, %rdi')
        add_asm('movq    %rax, -40(%rbp)')         
        add_asm('movq    %rcx, -48(%rbp)')         
        add_asm('movq    %rsi, -56(%rbp)')        
        add_asm('callq   _strlen')
        add_asm('movq    -48(%rbp), %rcx')         
        add_asm('subq    %rax, %rcx')
        add_asm('movq    -32(%rbp), %rdi')         
        add_asm('movq    -56(%rbp), %rsi')         
        add_asm('movq    %rcx, %rdx')
        add_asm('callq   _strncat')
        add_asm('movq    -24(%rbp), %rcx')
        add_asm('movq    %rax, -64(%rbp)')        
        add_asm('movq    %rcx, %rax')
        add_asm('addq    $64, %rsp')
        add_asm('popq    %rbp')
        add_asm('retq')
        add_asm('.globl  _main')


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
    table['syms'][s] = table['env']['count']
    table['env']['count'] += 1

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

    elif is_select_instruction(inst[1]):
        taverse_select_instruction(inst[1])

    elif is_iter_instruction(inst[1]):
        traverse_iter_instruction(inst[1])

    elif is_compound_instruction(inst[1]):
        traverse_compound_instruction(inst[1])
    
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
    global num_string
    global call_cat
    global exist_str
    if is_iconst(expr):
        _, n = expr
        add_asm('pushq $%s' %(n))

    if is_sconst(expr):
        _, string = expr
        num_string = num_string + 1
        add_asm('leaq L_.str'+str(num_string)+'(%rip), %rcx')
        add_asm('pushq %rcx')
        string_ins.append(('L_.str'+str(num_string)+':'))
        string_ins.append('.asciz '+str(string))
        exist_str = True

    if is_id(expr):
        _, x = expr
        add_asm('pushq %s' %(addr_of_sym(x)))

    elif is_func_call(expr):
        _, (_, f), args = expr

        if f == 'printd':
            assert len(args) == 1
            expr = args[0]
            traverse_expression(expr) 
            add_asm('popq %rax')
            add_asm('leaq L_.str(%rip), %rdi')
            add_asm('movl %eax, %esi')
            add_asm('movb $0, %al') 
            add_asm('callq _printf')

        elif f == 'sleep':
            assert len(args) == 1
            expr = args[0]
            traverse_expression(expr) 
            add_asm('popq %rdi') 
            add_asm('movb $0, %al')
            add_asm('callq _sleep')
        
        elif f == 'cat':
            assert len(args) == 2
            expr = args[0]
            traverse_expression(expr)
            add_asm('popq %rdi')
            expr2 = args[1]
            traverse_expression(expr2)
            add_asm('popq %rsi')
            # add_asm('movl $0, -4(%rbp)')
            add_asm('callq _cat')
            add_asm('pushq %rax')
            call_cat = True
        
        elif f == 'printf':
            assert len(args) == 1
            expr = args[0]
            traverse_expression(expr)
            add_asm('popq %rdi')
            add_asm('callq _printf')
            # add_asm('xorl %ecx, %ecx')
            # add_asm('movl %eax, -8(%rbp)')         
            # add_asm('movl %ecx, %eax')

        else:
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
        
        if op == 'MOD':
            add_asm('popq %rax')
            add_asm('pushq %rdx')

    elif is_neg_expr(expr):
        _, e = expr
        traverse_expression(e)
        add_asm('popq %rax')
        add_asm('negq %rax')
        add_asm('pushq %rax')

    elif is_primary_expr(expr):
        _, e = expr
        traverse_expression(e)

    elif is_shift_expr(expr):
        op, a, b = expr
        traverse_expression(a)
        traverse_expression(b)
        add_asm('popq %rcx')
        add_asm('popq %rax')
        add_asm('cltd') 
        add_asm('%s %%cl, %%eax' %('shll' if op == 'LSHIFT' else 'shrl'))
        add_asm('pushq %rax')

def taverse_select_instruction(inst):
    inst_id = 'BRANCH_%s' %(gen_id())

    if inst[0] == 'IF':
        _, pred, branch = inst
        cmp_op = traverse_condition(pred)
        add_asm('%s %s_END' %(op_to_cmd[cmp_op], inst_id))

        enter_block('%s_IF' %inst_id, 'local')
        traverse_instruction(branch)
        leave_block()

        add_asm('%s_END:' %inst_id)
    else:
        _, pred, branch_a, branch_b = inst
        cmp_op = traverse_condition(pred)
        add_asm('%s %s_ELSE' %(op_to_cmd[cmp_op], inst_id))

        enter_block('%s_IF' %inst_id, 'local')
        traverse_instruction(branch_a)
        leave_block()
        add_asm('jmp %s_END' %inst_id)

        add_asm('%s_ELSE:' %inst_id)
        enter_block('%s_ELSE' %inst_id, 'local')
        traverse_instruction(branch_b)
        leave_block()

        add_asm('%s_END:' %inst_id)

def traverse_iter_instruction(inst):
    inst_id = 'ITER_%s' %(gen_id())
    enter_block(inst_id, 'local')

    if inst[0] == 'WHILE':
        add_asm('%s_START:' %inst_id)

        _, pred, block = inst
        cmp_op = traverse_condition(pred)
        add_asm('%s %s_END' %(op_to_cmd[cmp_op], inst_id))

        traverse_instruction(block)

        add_asm('jmp %s_START' %inst_id)
        add_asm('%s_END:' %inst_id)

    elif inst[0] == 'FOR':
        _, init, pred, incr, block = inst
        traverse_instruction(('STAT', init))
        add_asm('%s_START:' %inst_id)

        cmp_op = traverse_condition(pred)
        add_asm('%s %s_END' %(op_to_cmd[cmp_op], inst_id))

        traverse_instruction(block)
        traverse_instruction(('STAT', incr))

        add_asm('jmp %s_START' %inst_id)
        add_asm('%s_END:' %inst_id)

    elif inst[0] == 'DO_WHILE':
        _, block, pred = inst
        add_asm('%s_START:' %inst_id)
        traverse_instruction(block)

        cmp_op = traverse_condition(pred)
        add_asm('%s %s_END' %(op_to_cmd[cmp_op], inst_id))
        add_asm('jmp %s_START' %inst_id)
        add_asm('%s_END:' %inst_id)

    leave_block()

def traverse_condition(pred):
    cmp_op, e1, e2 = pred
    traverse_expression(e1)
    traverse_expression(e2)
    add_cmp_asm('cmpq')
    return cmp_op

if __name__ == '__main__':
    parser = cparse.parser
    s = remove_blank(remove_comment(sys.stdin.read()))
    asts = parser.parse(s)

    enter_block('global')
    map(traverse_ast, asts)
    if_call_cat()
    if_exist_string()
    add_str_literal_asm()
    leave_block()

    print '\n'.join(instructions)
