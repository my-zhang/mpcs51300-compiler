
Compiler Design Part I – Parsing
================================

Mengyu Zhang mengyuzhang@uchicago.edu
Xiang Li lix1@uchicago.edu

- `sample.c` sample C source code;
- `preprocess.py` comments and empty lines removing;
- `lex.py` libray module copied from [PLY](http://www.dabeaz.com/ply/);
- `tokenize.py` tokenizer module.

Preprocess
----------

Sample C source code.

```c
// External function extern 
extern int foo2(int x); 

/* Function 
 * a foo func
 */
int foo(int count /*cnt */)
{
    //invalid input
    //int #$@0_illegal = 1
    int sum = 0.0; // init sum to 0
    for (int i = 1; i <= count; i++) 
        sum += foo2(i); 
    return sum; 
}
```

```
$ cat sample.c | python preprocess.py > out.c
```

Output

```c
extern int foo2(int x);
int foo(int count )
{
int sum = 0.0;
for (int i = 1; i <= count; i++)
sum += foo2(i);
return sum;
}
```


Tokenize
--------

```
$ cat out.c | python tokenize.py 
extern 	:	EXTERN
int 	:	INT
foo2 	:	ID
( 	:	LPAREN
int 	:	INT
x 	:	ID
) 	:	RPAREN
; 	:	SEMICOLON
int 	:	INT
foo 	:	ID
( 	:	LPAREN
int 	:	INT
count 	:	ID
) 	:	RPAREN
{ 	:	LBRACE
int 	:	INT
sum 	:	ID
= 	:	ASSIGN
0.0 	:	FLOAT
; 	:	SEMICOLON
int 	:	INT
int1 	:	ID
= 	:	ASSIGN
1.0 	:	NUMBER
; 	:	SEMICOLON
for 	:	FOR
( 	:	LPAREN
int 	:	INT
i 	:	ID
= 	:	ASSIGN
1.0 	:	NUMBER
; 	:	SEMICOLON
i 	:	ID
<= 	:	LE
count 	:	ID
; 	:	SEMICOLON
i 	:	ID
+ 	:	ADD
+ 	:	ADD
) 	:	RPAREN
sum 	:	ID
+= 	:	ADD_ASSIGN
foo2 	:	ID
( 	:	LPAREN
i 	:	ID
) 	:	RPAREN
; 	:	SEMICOLON
return 	:	RETURN
sum 	:	ID
; 	:	SEMICOLON
} 	:	RBRACE
```

