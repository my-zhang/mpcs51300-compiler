Compiler Design Part II – Parsing
=================================

This is the 2nd part of the parsing project, which constructs symbol table(with scope) and commands list.

Contributors
------------

Mengyu Zhang mengyuzhang@uchicago.edu

Xiang Li lix1@uchicago.edu

Run
---

To parse a source file, just do,

```
$ ls
README.md   hw02        sample.c    setup.py    test

$ python -m hw02.main < sample.c

Define extern function with name bar
Define variable with type int and name sum
Define variable with type string and name s
Define variable with type int and name i
Assign i
Call Function bar
Assign sum
Define Iteration with variable i
Return  sum
Define function with name foo

============ SYMBOL TABLE ============
count   int                  foo
bar     int                  extern
i       int                  foo
sum     int                  foo
s       string               foo
x       int                  extern$bar
foo     ('FUNC', 'int')      global
```

Test
----

Unit tests are implemented in dir `test`.

```
$ ls test/
__init__.py test_dec.py test_math.py
```

To run test, just do,

```
$ python setup.py test
```

Since we're using py.test framework, so py.test is required. To install,

```
$ sudo pip install -U pytest
```

Project Structure
-----------------

```
├── README.md
├── hw02                        # core source file diretory
│   ├── __init__.py
│   ├── clex.py                     # tokenizer
│   ├── cparse.py                   # parser
│   ├── main.py                     # entry point of the program
│   ├── ply                         # 
│   │   ├── __init__.py             # 
│   │   ├── lex.py                  # PLY library
│   │   └── yacc.py                 # 
│   └── preprocess.py               # preprocessor
|
├── sample.c                    # sample input file
├── setup.py                    # 'makefile' for python project
└── test                        # test directory
    ├── __init__.py
        ├── test_dec.py
            └── test_math.py
```

