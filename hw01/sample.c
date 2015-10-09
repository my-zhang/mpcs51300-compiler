// External function extern 
extern int foo2(int x); 

/* Function 
 * a foo func
 */
int foo(int count /*cnt */) 
{ 
    int sum = 0.0; // init sum to 0
    for (int i = 1; i <= count; i++) 
        sum += foo2(i); 
    return sum; 
}
