As mentioned in the overview, as long as we can (1) compile your program via `make`, (2) run your program as described, and (3) successfully compress + uncompress a file, you are absolutely free to implement the project any way you think is best. However, here are some suggestions just in case you feel a bit lost.

# Suggested Development Process
Before doing anything, it is a good idea to create all required `.cpp` files (see the `Makefile`) and write blank `main()` functions in your `compress.cpp` and `uncompress.cpp` files to get your project files to the point that you can compile successfully with `make` (even though the `compress` and `uncompress` executables don't do anything). Once you get things compiling, start working on `compress`, and once you are confident that you have that working reasonably well, start working on `uncompress`. Use print statements, `gdb`, etc. as you develop to make sure you're implementing things correctly.

## *Suggested Control Flow for `compress`*
1. Parse the command line arguments and throw an error message if the user runs your program incorrectly
2. Open the input file for reading
3. Read bytes from the file. Count the number of occurrences of each byte value
4. Use the byte counts to construct a Huffman coding tree. Each unique byte with a non-zero count will be a leaf node in the Huffman tree
5. Open the output file for writing
6. Write enough information (a "file header") to the output file to enable the coding tree to be reconstructed when the file is read by your `uncompress` program
7. Move back to the beginning of the input file to be able to read it, again
8. Using the Huffman coding tree, translate each byte from the input file into its code, and append these codes as a sequence of bits to the output file, after the header
9. Close the input and output files (note that this is handled for you; see "Design Notes")

## *Control Flow for `uncompress`*
1. Open the input file for reading
2. Read the file header at the beginning of the input file, and use it to reconstruct the Huffman coding tree
3. Open the output file for writing
4. Using the Huffman coding tree, decode the bits from the input file into the appropriate sequence of bytes, writing them to the output file
5. Close the input and output files (note that this is handled for you; see "Design Notes")

# Potential Development Process
If you choose to use the code structure we have laid out in the starter, one reasonable potential development process is the following. Note that this is independent of the "Suggested Development Process" section, which gives an overview of how a functioning `compress.cpp` and `uncompress.cpp` (the source code) should *look* like. This section illustrates our suggested steps to go from the starter code to a functioning `compress` and `uncompress` (the executables):

1. Create `compress.cpp` and `uncompress.cpp` with `main()` functions that don't do anything for now
    * This will allow you to compile your program as you make changes to the other files
    * As you implement the components described below, you can use your `main()` functions in `compress.cpp` and `uncompress.cpp` to test them out one-by-one
    * For right now, think of `compress.cpp` and `uncompress.cpp` as blank canvases to be able to write code to test the other components, and you will write the actual implementation of both programs later
2. Create `HCTree.cpp` and add skeletons of the `HCTree` functions you will need to implement
    * Refer to `HCTree.hpp` to see what function signatures are declared in the `HCTree` class
3. Implement the `HCTree::build` function to construct a Huffman Tree from symbol frequencies
    * You will want to use `gdb` or print statements to help you trace your tree to make sure it matches what you would get if you constructed it manually by hand (on small example files)
4. Implement the `HCTree` destructor
5. Implement the `HCTree::encode` function to encode a given symbol
6. Implement the `HCTree::decode` function
7. Once you are confident that all of the individual components are working properly, begin to piece them together in the `main` functions of `compress.cpp` and `uncompress.cpp` according to the suggested control flows above
    * Incorporate one step of the control flow, then test it thoroughly to make sure things work to that point, then incorporate the next step, test thoroughly, etc.
    * How you choose to implement your compressed file header is up to you, but we have some recommendations in the "Design Notes" section, so be sure to refer to that

# Map Out *Your* Ideal Approach
As mentioned, the above suggested control flows and development processes are simply what *we* recommend if you feel lost and don't know where to start. However, *not everybody thinks/works the same!* What we suggest may not be the best approach for you personally. Before you even write a single line of code, read through this guide and make sure you fully understand the required tasks of the project, and then actually sit down and map out how *you personally* want to approach the problem. You are of course free to deviate from or modify the programming approach you design, but simply having a roadmap to help guide you can be *extremely* helpful when coding.

**TL;DR:** Try not to write a *single line of code* until you actually physically map out how you personally want/plan to approach this project! Feel free to chat with a tutor during Lab Hours if you want some feedback about your approach! :-)
