Originally written by [Ronak Shah](https://ronakshah.org/)\
Additions made by [Aatash Pestonjamasp](https://www.linkedin.com/in/aatash-pestonjamasp)

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

This will then give you a line number where the issue is, or tell you what's going on. 

## Unfamiliar Code

Once you encounter the seg fault after running, you may encounter an unfamiliar 
line of code, an example of which is shown below:

```
Program received signal SIGSEGV, Segmentation fault.
0x00005586d963f990 in std::_Hashtable<char, std::pair<char const, TestSet::Node*>, std::allocator<std::pair<char const, TestSet::Node*> >, std::__detail::_Select1st, std::equal_to<char>, std::hash<char>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::size (this=0x8)
    at /usr/include/c++/12/bits/hashtable.h:649
649           { return _M_element_count; }
```

Fear not! Your code simply may have made a system call incorrectly where the 
actual segmentation fault occurred. You will need to investigate what in your code
caused a system or other function call to be made incorrectly.

At this point, you will want to look into your code, by printing values, etc, but
may find that your variables are out of scope; gdb has taken you to the "deeper
level" system calls. To travel to your function's scope, you can run `bt` (or `backtrace`)  
to view the entire call stack. You will see  numbers next to each function indicating 
the level of the stack it was made from. 

Once you find the number corresponding to your code, you can type `up` to move 
back up the function call stack until you reach your code, and `down` if you 
want to move to lower levels at any point. You may also type `frame` followed by 
the stack frame number (for example `frame 3`) to select the stack frame of the function designated with #3 by `backtrace`). From there, you can commence your debugging!


More help on GDB — Check out the [GDB Cheatsheet](GDB%20Cheatsheet.md)!
