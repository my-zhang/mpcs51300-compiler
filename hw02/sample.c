
extern int bar(int x);

int foo(int count) {
    float sum = -2.2;
    string test = "haha";
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
