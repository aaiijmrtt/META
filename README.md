#META

Functional Metaprogramming in C++

The code in this repository presents a Turing-complete functional metaprogramming wrapper for C++. Valid C++ source code as input to the metaprogrammer will result in valid C++ source code as output. Detailed language specifications will follow in later stages of development. Some preliminary samples have been provided, demonstrating basic conditional and iterative constructs.

**Instructions**:

1. **Generate Source Code From Metaprogram**: eg. `$python metaprogrammer.py < factorial.mp > factorial.cpp`

2. **Include Generated Source Code in Target Source Code**: eg. `#include "factorial.cpp"`

3. **Compile Target Source Code**: eg. `$g++ -o factorial program.cpp`

4. **Execute Target Object Code**: eg. `$./factorial`

**Sample Code**:

1. **To calculate the factorial of a number**:

  1. Store a simple recursive definition for the factorial function in a file named `factorial.mp`. Add a newline at end of each function.

          factorial(n) = int : int
           = 1 :: n <= 1
           = n * factorial(n - 1)

  2. Store the target source code in a file named `program.cpp`:

          #include <cstdio>
          #include "factorial.cpp"
          int main(int argc, char **argv) {
            printf("%d\n", factorial(12));
            return 0;
          }

  3. Generate, Compile, Execute:

          $python metaprogrammer.py < factorial.mp > factorial.cpp
          $g++ -o factorial program.cpp
          $./factorial

2. **To calculate the fibonacci series**:

  1. Store a simple recursive definition for the fibonacci function in a file named `fibonacci.mp`. Top Down Memorization support is enabled. Add a newline at end of each function.

          fibonacci(n) = int[0, 45] : int[-1]
           = 1 :: n <= 2
           = fibonacci(n - 1) + fibonacci(n - 2)

  2. As an alternative to writing the target program, store a simple target metaprogram in a file named `program.mp`. Add a newline at end of each function.

          #include <cstdio>
          #include "fibonacci.cpp"
          main(argc, argv) = int char** : int
           int i;
           printf("%d\n", fibonacci(i)); :: i[1, 45, +]
           return 0;

  3. Generate, Compile, Execute:

          $python metaprogrammer.py < fibonacci.mp > fibonacci.cpp
          $python metaprogrammer.py < program.mp > program.cpp
          $g++ -o fibonacci program.cpp
          $./fibonacci

**Note**:

* Requires Python.
* Requires Pyparsing.
* Requires g++.
