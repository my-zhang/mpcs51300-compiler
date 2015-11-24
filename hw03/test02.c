
int foo(int b) {
    int a;
    a = 1;
    return a + b;
}

int bar(int x, int y) {
    return x * y;
}

int main() {
    int x;
    int y;
    x = 2;
    y = 5;
    return foo(2) + bar(x, y);
}
