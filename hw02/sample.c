
int foo(int count) {
    int sum = 2;
    int i;
    for(i = 1; i<=count; i++) 
        sum = sum + bar(i);
    return sum; 
}
