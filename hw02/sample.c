
extern int bar(int x);

int foo(int count) {
    int sum = 1;
    string s = "haha";

    int i;
    for(i = 1; i <= count; i++)
        sum = sum + bar(i);

    return sum; 
}
