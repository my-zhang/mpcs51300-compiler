Compiler Design Part III
========================

This is the 3rd part of the parsing project.

Contributors
------------

Mengyu Zhang mengyuzhang@uchicago.edu

Xiang Li lix1@uchicago.edu

Run
---

To compile a source file into asm, and then executable,

```
$ python -m hw02.gen_asm < sample.c > a.s
$ gcc a.s
./a.out
$ echo $?
```
