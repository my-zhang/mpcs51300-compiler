
Assignment 3
============

Exercise 1
----------

Let's consider the following context-free grammar defined by the following rules.

```
S -> I; S | ε 
I -> E | ε
E -> E + T | E – T | T
T -> T * F | T / F | F
F -> const | (E)
```


### Question 1

Draw a derivation tree for:

- 5+3*2;

```
S -> I; S
  -> E; S
  -> E + T; S
  -> T + T; S
  -> F + T; S
  -> const + T; S
  -> const + T * F; S
  -> const + F * F; S
  -> const + const * F; S
  -> const + const * const; S
  -> const + const * const; ε
```

- 3;2/3*(1-3);

```
S -> I; S
  -> E; S
  -> T; S
  -> F; S
  -> const; S
  -> const; I; S
  -> const; E; S
  -> const; T; S
  -> const; T * F; S
  -> const; T / F * F; S
  -> const; F / F * F; S
  -> const; const / F * F; S
  -> const; const / const * (E); S
  -> const; const / const * (E - T); S
  -> const; const / const * (T - T); S
  -> const; const / const * (F - T); S
  -> const; const / const * (const - T); S
  -> const; const / const * (const - F); S
  -> const; const / const * (const - const); S
  -> const; const / const * (const - const); ε
```

### Question 2

Does this grammar have a left-most derivation? If so, can you transform this grammar into a right-most derivation?

I'm a little confused about this question. 

According to my understanding, grammar has no concept of leftmost or rightmost, which is actually determined by parsing techniques. As following example from dragon book, where the same sentence of the same grammar generates a rightmost derivation by shift-and-reduce(bottom-up). However it does also have a leftmost derivation when talking about top-down parsing previously.

<img src="/doc/images/assignment_03_left_right_most.png"/>

### Question 3

Implement this grammar using the library of your choice and calculate the following expression:

- 3*(1+2)/(1);

Implemention in `calc.py`

```
$ echo "3;2/3*(1-3);5+3*2;" | python calc.py
[3, 0, 11]
$ 
$ echo "3*(1+2)/(1);" | python calc.py
[9]
```


Exercise 2
----------

Let's consider the following grammar.

```
E -> E + T
E -> T
T -> T * F
T -> F
F -> (E)
F -> nb
```

### Question 1

Use this table to recognize.

<img src="/doc/images/assignment_03_table.png"/>

- 3+*4

```
STACK     | RULE
----------+-----
0         | 
nb 5      | 
0 F 3     | F -> nb
0 T 2     | T -> F
0 E 1     | E -> T
6 + 1 E 0 | 
        ERROR
```

- (3+4)*5

```
STACK               | RULE
--------------------+-------------
0                   |
0 ( 4               |
0 ( 4 nb 5          |
0 ( 4 F 3           | F -> nb
0 ( 4 E 8           | E -> F
0 ( 4 E 8 + 6       |
0 ( 4 E 8 + 6 nb 5  |
0 ( 4 E 8 + 6 F 3   | F -> nb
0 ( 4 E 8 + 6 T 9   | T -> F
0 ( 4 E 8 ) 11      | E -> E + T
0 F 3               | F -> ( E )
0 T 2               | T -> F
0 T 2 * 7           |
0 T 2 * 7 nb 5      |
0 T 2 * 7 F 10      | F -> nb
0 T 2               | T -> T * F
0 E 1               | E -> T
0                   | ACC
```

### Question 2

Implement this grammar using the library of your choice

Implemented in `expr.py`, with imported library **PLY** files `lex.py` and `yacc.py` in directory `ply`.

```
$ echo "(3+4)*5" | python expr.py
35
```

### Question 3

Propose some semantic actions to calculate the value of an arithmetic expression.

As implemented in Question 2, semantic actions are intuitively arithmatic operations. 

```
E -> E + T      E.val = E.val + T.val
E -> T          E.val = T.val
T -> T * F      T.val = T.val * F.val
T -> F          T.val = F.val
F -> (E)        T.val = E.val
F -> nb         F.val = int(nb)
```
