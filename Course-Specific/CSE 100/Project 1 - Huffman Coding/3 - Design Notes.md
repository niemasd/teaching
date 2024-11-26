Before you write even a single line of code, it's important to properly design the various components of your `compress` and `uncompress` programs. Here, we will discuss some aspects of the design that you should be sure to think about.

# Parsing Command Line Arguments in C++
Remember that, in C++, you can parse command line arguments by writing a `main` function as follows:

```cpp
int main(int argc, char* argv[]) {
    // your program's main execution code
}
```

The `argc` variable provides the number of command line arguments that were provided, and the `argv` variable is an array containing the command line arguments. See [this article](http://www.cplusplus.com/articles/DEN36Up4/) to learn more about how to use them.

# File I/O
For this assignment, you will have to read data from files and write data to files. To help you with this, in `Helper.hpp` and `Helper.cpp`, we have provided two helper classes that can make it easier to perform file I/O: `FancyInputStream` and `FancyOutputStream`. It is up to you to thoroughly read the header comments of the functions in these two classes to see how to use them. It is a good idea to have the "Project Workflow" open while you look at the function headers for `FancyInputStream` and `FancyOutputStream` to get a better idea of how you can apply various functions of those classes to the `compress` and `uncompress` workflows.

Note that, in C++, `ifstream` and `ofstream` objects are automatically closed by their destructors. Thus, when a `FancyInputStream` or `FancyOutputStream` object is destroyed (e.g. if you create it on the runtime stack and it goes out of scope), the internal `ifstream`/`ofstream` object will also automatically get destroyed (and thus will automatically close).

# Huffman Tree
One crucial data structure you will need is a **binary trie** (i.e., "code tree" or "encoding tree") that represents a Huffman code. The `HCTree.hpp` header file provides a possible interface for this structure (included in your repo as skeleton code); you can modify this in any way you want.

Additionally, you will write a companion `HCTree.cpp` implementation file that implements the interface specified in `HCTree.hpp`, and you will then use it in your `compress` and `uncompress` programs. Note that, when you implement the `HCTree` class, you will want to use the `HCNode` class we have provided in `Helper.hpp`.

As you implement Huffman's algorithm, you will find it convenient to use multiple data structures. For example, a priority queue will assist in building the Huffman Tree. Feel free to utilize other beneficial data structures. However, you should use good object-oriented design in your solution. For example, since a Huffman code tree will be used by both your `compress` and `uncompress` programs, it makes sense to encapsulate its functionality inside a single class accessible by both programs. With a good design, the `main` functions in the `compress` and `uncompress` programs will be quite simple: they will create objects of other classes and call their methods to do the necessary work.

Be sure to refer to the ["Honey, I Shrunk the File"](https://cogniterra.org/lesson/37561) section of the *Data Structures* Cogniterra text for more information about Huffman's algorithm.

## *Priority Queues in C++*
A C++ `priority_queue` is a generic container that can hold any type, including `HCNode*` (wink wink). By default, a `priority_queue<T>` will use the `<` operator defined for objects of type `T`. Specifically, if `a < b`, then `b` is taken to have a **higher priority** than `a` (i.e., by default, it functions as a **max**-heap).

However, in the Huffman Tree building algorithm, we want to select symbols with ***lower* frequencies first** (i.e., we want to use a **min**-heap). Thus, we need to tell the `priority_queue` how to compare `HCNode*` objects by defining a custom "comparison class" that will dereference the pointers and compare the objects they point to. This has been done for you via the `HCNodePtrComp` class in `Helper.hpp`. You can use it to create a `priority_queue` as follows:

```cpp
priority_queue<HCNode*, vector<HCNode*>, HCNodePtrComp> pq;
```

* The first argument of the template (`HCNode*`) tells the `priority_queue` that it will be storing `HCNode*` objects
* The second argument of the template (`vector<HCNode*>`)  tells the `priority_queue` to use a `vector<HCNode*>` container behind-the-scenes to store its elements
* The third argument of the template (`HCNodePtrComp`) tells the `priority_queue` to use our custom `HCNodePtrComp` class when comparing `HCNode*` objects to determine priorities

Be sure to refer to the [C++ `priority_queue` documentation](http://www.cplusplus.com/reference/queue/priority_queue/) for more information about how to use a `priority_queue`.

# Compressed File Header
In the "Suggested Control Flow" section, you will see references to a header that should be stored by the `compress` program and later retrieved by the `uncompress` program. Both the `compress` and `uncompress` programs need to construct the Huffman Tree before they can successfully encode and decode information, respectively. The `compress` program has access to the original file, so it can build the tree by first deciphering the symbol counts. However, the `uncompress` program only has access to the compressed file, not the original file, so it has to use some other information to build the tree. The information needed for the `uncompress` program to build the Huffman Tree needs to be stored in the header of the compressed file. In other words, the header information should be sufficient to reconstruct the tree.

## *Efficient Header Design*
One extremely *inefficient* strategy for designing the header (which is what is used in the reference solution) is to simply store 256 integers (in 4-byte chunks as `unsigned int` objects) at the beginning of the compressed file (i.e., encode the symbol counts as the header), but note that this is not very efficient and is guaranteed to use up 256*4 = 1024 bytes! In order to receive full points, you must BEAT our reference solution by coming up with a more efficient way to represent this header!

However, we **strongly** encourage you to implement the naïve (256 `unsigned int` objects) approach first, and do not attempt to reduce the size of the header until you’ve gotten your `compress` and `uncompress` to work correctly for the provided inputs.

One way to reduce the size of the header is to take a frequency approach, but to think about how many bytes you *really* need to store each integer. Answering this question relates to the maximum size of the files that you are required to encode: your `compress` program must work for input files up to 10 MB in size, so a particular byte value may occur up to ~10 million times in the file. This fact should help you determine the minimum number of bytes required to represent each frequency count in you header.

Alternative approaches may use arrays to represent the structure of the tree itself in the header. With some cleverness, it is possible to optimize the header size to about 10*M* bits, where *M* is the number of distinct byte values that actually appear in the input file. [This write-up](https://www.baeldung.com/cs/binary-tree-serialize-deserialize) may be helpful to learn about how to "serialize" the tree structure itself.
