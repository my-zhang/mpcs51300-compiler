
extern int foo2(int x);

int foo(int count) {
    int sum = 0.0;
    int i;
    for(i=1; i<=count; i++) 
        sum = sum + foo2(i);
    return sum; 
}
