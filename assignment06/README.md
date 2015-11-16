
Assignment 6
============

Exercise
--------

Let's consider the following context-free grammar. We are creating a calculator handling identifiers.

```
S -> I; S | ε 
I -> ident := E | E | ε
E -> E + T | E – T | T
T -> T * F | T / F | F
F -> ident | const | (E)
```

### Question 1

> Propose a simple data structure to allow the compiler to represent and handle internally an assembly code.

I make assembly code stored in a list, which each assembly instruction is a tuple of the format (opcode, oprand1, oprand2).

### Question 2

> Where can you store the variables?

I used a hashmap to track the position of each variable that will be placed on the stack. 

For exmaple, if `"a:=6; b:=9; a+b;"`, then the hashmap will be like `{a: -4, b: -8}`, and thus `a` and `b` will locate at `-4(%ebp)` and `-8(%ebp)`.

### Question 3

Implemented in `p3.py`, with lib files in dir `ply`. 

**X86-64 Mac** platform required.

Simple example:

```
$ echo "a:=1; a+2;" | python p3.py > a.s
$ gcc a.s
$ ./a.out
Ans: 3
```

The content of generated assembly file.

```assembly_x86
.globl _main
_main:
pushq %rbp
movq %rsp, %rbp
subq $256, %rsp
pushq $1
popq -8(%rbp)
pushq -8(%rbp)
pushq $2
popq %rbx
popq %rax
cltd
addq %rbx, %rax
pushq %rax
popq %rax
leaq L_.str(%rip), %rdi
movl %eax, %esi
movb $0, %al
callq _printf
addq $256, %rsp
popq %rbp
retq
.section __TEXT,__cstring,cstring_literals
L_.str:
.asciz "Ans: %d\n"
```

A complicated case:

```
$ echo "a:=1; b:=2; (a+b)*(3-4); a+6/3-b;" | python p3.py > a.s
$ gcc a.s
$ ./a.out
Ans: -3
Ans: 1
```
