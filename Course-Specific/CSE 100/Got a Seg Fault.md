Originally written by [Ronak Shah](https://ronakshah.org/)

# Got a Seg Fault?
In your C/C++ programming endeavors, you'll often see a scary error message from time to time:

```
[1] 3715 segmentation fault ./a.out
```

This is called a **segmentation fault**, and it's a somewhat common error in C/C++ programming.

## Why segmentation faults happen
From [Wikipedia](https://en.wikipedia.org/wiki/Segmentation_fault#Overview):

> A segmentation fault occurs when a program attempts to access a memory location that it is not allowed to access, or attempts to access a memory location in a way that is not allowed.

More simply put, we run into these errors whenever we try to access something that doesn't exist. This can take many forms, whether it's array out of bounds or dereferencing a null pointer. 

# Narrowing down where it's happening
GDB is your friend! If you're getting a segmentation fault when you run the program on something, try loading it into GDB — when it fails, it will often tell you the line where it failed, which you can then use to resolve the issue.

For example, if you were getting a segmentation fault by running the following command:

```bash
$ ./someProgram arg1 arg2
```

You can run it instead using GDB by doing the following:

```bash
$ gdb someProgram
(gdb) run arg1 arg2
```

This will then give you a line number where the issue is, or tell you what's going on. If you don't see anything, run `bt` (or `backtrace`) to view the entire call stack.

More help on GDB — Check out the [GDB Cheatsheet](GDB Cheatsheet.md)!
