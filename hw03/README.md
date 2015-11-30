Compiler Design Part III
========================

This is the 3rd part of the parsing project.

Contributors
------------

Mengyu Zhang mengyuzhang@uchicago.edu

Xiang Li lix1@uchicago.edu

Completeness
------------

Have passed all the testcases in dir `tests/` which doesn't include *string* and *array*.

Run
---

To compile a source file into asm, and then executable,

```
$ ls
README.md   hw03        setup.py    tests

$ python -m hw03.gen_asm < tests/add.c > add.s

$ gcc add.s

./a.out
44877
44877
45123
45123
44877
44877
44877
45123
44877
```

Project Structure
-----------------

```
├── README.md
├── hw03
│   ├── __init__.py
│   ├── clex.py
│   ├── cparse.py           # grammar and AST
│   ├── gen_asm.py          # entry point
│   ├── ply
│   │   ├── __init__.py
│   │   ├── lex.py
│   │   └── yacc.py
│   └── preprocess.py
├── setup.py
└── tests                   # testcases
    ├── add.c
    ├── compteur.c
    ├── cond.c
    ├── div.c
    ├── expr.c
    ├── functions.c
    ├── loops.c
    ├── lsh.c
    ├── mod.c
    ├── mul.c
    ├── neg.c
    ├── rsh.c
    ├── sub.c
    └── toto.c
```
