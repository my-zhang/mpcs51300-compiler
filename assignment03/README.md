
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
- 3;2/3*(1-3);


### Question 2

Does this grammar have a left-most derivation? If so, can you transform this grammar into a right-most derivation?

This a corresponding LL(1) grammar, which generates a left-most derivation when using top-down parsing.

```
S   -> E S' | ε
S'  -> ; S
E   -> T E'
E'  -> [+-] T E' | ε
T   -> F T'
T'  -> [*/] F T' | ε
F   -> const | (E)
```

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
- (3+4)*5


### Question 2

Implement this grammar using the library of your choice


### Question 3

Propose some semantic actions to calculate the value of an arithmetic expression.

