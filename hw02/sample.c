
extern int bar(int x);

int foo(int count) {
    int sum = 2;
    int i;
    int a;
    for(i = 1; i <= count; i++)
        sum = sum + bar(i);

    for(i = 1; i <= count; i++) {
        int a = i * i;
        sum += a;
    }
    return sum; 
}
