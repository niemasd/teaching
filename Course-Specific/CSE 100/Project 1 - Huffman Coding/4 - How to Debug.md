As you work on this Project, you will almost certainly run into bugs you will need to find and fix. Because of the bitwise nature of this Project, debugging might be more challenging than usual. Here, we will provide some general tips for debugging that may prove useful.

# Printing a Huffman Tree
As you implement the Huffman Tree components of `compress` and `uncompress`, you will want to verify that the Huffman Tree you built is correct by working through the exact same example by hand and manually comparing the tree your code builds against the tree you manually build by hand. To compare the tree your code builds against the tree you built yourself, you will want to somehow view the Huffman Tree in your code. We suggest doing this in one of the following two ways:

* Write a helper function that traverses an `HCTree` object and outputs the edges in some human-readable format (e.g. as an edge list you can then draw out by hand)
* Use `gdb` to set a breakpoint just after the `HCTree` object is built, and use `gdb` commands to print the entire tree (e.g. as an edge list you can then draw out by hand)

# Viewing a Binary File as Bits
As you implement `compress`, you will likely want to try compressing a small example file that you can trace by hand and then manually look at the compressed output file to verify that it looks like what you would expect. However, if you try to open the binary file in `vim` or similar, you will likely see garbage data: the text editor is trying to render each byte as a human-readable character (and is failing to do so).

Instead, you can view the bit representation of a binary file using a hex dump tool. One good choice is `xxd`, which is a command-line hex dump tool that exists on most Linux distributions. Given any arbitrary file (plain-text or binary!), you can call `xxd` with the `-b` flag (for "bits") to view the bit representation of the bytes in the file. For example, if I have a file [`combooter.txt`](https://www.mariowiki.com/List_of_Boos_in_Luigi%27s_Mansion:_Dark_Moon#Old_Clockworks) that contains the text `boo` (3 bytes), I can view the binary representation of the file as follows:

```bash
$ xxd -b combooter.txt
00000000: 01100010 01101111 01101111                             boo
```

If the file you are trying to look at is very large, the output of `xxd` will be extremely long, so to make it easier to read through it, you can pipe the output of `xxd` to `less` to allow you to scroll up and down:

```bash
$ xxd -b combooter.txt | less
00000000: 01100010 01101111 01101111 00001010 01100010 01101111  boo.bo
00000006: 01101111 00001010 01100010 01101111 01101111 00001010  o.boo.
0000000c: 01100010 01101111 01101111 00001010 01100010 01101111  boo.bo
00000012: 01101111 00001010 01100010 01101111 01101111 00001010  o.boo.
00000018: 01100010 01101111 01101111 00001010 01100010 01101111  boo.bo
0000001e: 01101111 00001010 01100010 01101111 01101111 00001010  o.boo.
00000024: 01100010 01101111 01101111 00001010 01100010 01101111  boo.bo
0000002a: 01101111 00001010 01100010 01101111 01101111 00001010  o.boo.
00000030: 01100010 01101111 01101111 00001010 01100010 01101111  boo.bo
00000036: 01101111 00001010 01100010 01101111 01101111 00001010  o.boo.
0000003c: 01100010 01101111 01101111 00001010 01100010 01101111  boo.bo
:
```

# Speeding Up Code
If your code is taking too long to run, you will want to investigate *which parts* of your code are slow so you can speed up those specific parts. On pretty much any Linux platform, you can use `gprof` (**G**NU **Prof**iler) to perform "per-function profiling". There are more complicated profiling tools that exist, so if you feel comfortable learning how to set up / use one of those, feel free, but `gprof` works for me. The basic workflow is as follows:

```bash
$ make gprof             # Step 1: Compile your program with the -pg flag (we provide a Makefile target for convenience)
$ ./my_exe               # Step 2: Run your program (it will create a file gmon.out)
$ gprof my_exe | less -S # Step 3: Run gprof to profile (I pipe to less -S to make it easier to read)
```

The `gprof` output tells you what percentage of your runtime was spent on each function that was called in your code. Note that the profiling results will likely be uninformative on small datasets because the overall runtime will be too small, so you will want to design larger test datasets of your own to get more meaningful profiling results. Many times, the runtime will be some built-in C++ STL function, so you may think "Well, that's not my code, so that's not something I can speed up", but that would be incorrect! If a built-in C++ STL function is taking a bunch of runtime, it's because *you're calling* that function :-) So try to find where in your code you're calling it a bunch of times, and try to refactor that part of your code! Feel free to refer to [this lengthier tutorial about `gprof`](https://www.thegeekstuff.com/2012/08/gprof-tutorial/).
