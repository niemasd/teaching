# Plain-Text Files Ending with Newline Characters
Try using a text editor like `vim` to create a text file `niema.txt` that contains only the string `Niema` in it, and save the file. What is the file size? Intuitively, you might think that the size is 5 bytes (each character takes exactly 1 byte), but try running `ls -l` or `du -sb` to get the file size in bytes, and the results might surprise you:

```bash
$ du -sb niema.txt
6       niema.txt
```

As can be seen, the file is 6 bytes, not 5! What's going on? Let's look at the file using `xxd`:

```bash
$ xxd -b niema.txt
00000000: 01001110 01101001 01100101 01101101 01100001 00001010  Niema.
```

This shows us the following bytes:

```
01001110 =  78 = N
01101001 = 105 = i
01100101 = 101 = e
01101101 = 109 = m
01100001 =  97 = a
00001010 =  10 = NEWLINE (\n)
```

We see that, even though we didn't explicitly add a newline character (`\n`) to the end of our file, `vim` went ahead and added one for us. The reason why `vim` and most text editors do this by default is that, according to the [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_206), a "line" of plain-text is defined as "a sequence of zero or more non-newline characters plus a terminating newline character."

In your final implementation, you will need to support *all* possible bytes, including the newline character, but as you begin the Project, you may want to only play around with visible human-readable symbols. If you want to create plain-text files without a newline character at the end, you will want to use the `echo` command with the `-n` flag (which tells `echo` not to add a newline character at the very end), and redirect the output to a file using `>`:

```bash
$ echo -n "Niema" > niema_no_newline.txt
$ du -sb niema_no_newline.txt
5       niema_no_newline.txt
$ xxd -b niema_no_newline.txt
00000000: 01001110 01101001 01100101 01101101 01100001           Niema
```

# Unicode Characters
In general, we typically think of a single character in a plain-text file as a `char`, which is 1 byte (8 bits), meaning there are 2⁸ = 256 possible characters. However, let's imagine creating a plain-text file containing the string `ŇĩēѪą`:

```bash
$ echo -n "ŇĩēѪą" > niema_fancy.txt
```

You may expect this file to be exactly 5 bytes, as there are exactly 5 characters, right? However, manually checking the file size may surprise us:

```bash
$ du -sb niema_fancy.txt
10      niema_fancy.txt
```

Why is our file 10 bytes instead of 5? The issue is that we are using symbols from the extended [Unicode alphabet](https://en.wikipedia.org/wiki/List_of_Unicode_characters): basically, a single byte can only represent 256 possible symbols, so under the [Unicode encoding](https://en.wikipedia.org/wiki/Unicode), a single character in the extended alphabets can be represented using more than 1 byte. In this specific example, each of our 5 symbols (`ŇĩēѪą`) is represented using 2 bytes, which is why the file size is 10 bytes.

Just as a heads-up, you don't need to (and shouldn't try to) handle the multi-byte extended Unicode symbols as single symbols: if your `compress` and `uncompress` tools simply treat every file they encounter as files over the alphabet of all 256 possible bytes, they will be able to handle any arbitrary possible file completely fine.

# No Space Left On Device
This message means that your virtual environment has run out of disk space. This typically implies that you've accidentally created a massive file that's filled up your disk space. One common cause (but not necessarily the only cause) is that a loop in your code within which you're writing to disk is running too long (e.g. potentially an infinite loop). You will need to find out which file(s) are too large and delete them using the `rm` command.

You find out which files are largest using the `du` command (`-h` is for human-readable file size units, e.g. `M` for megabyte, and `-a` is to view *all* files, including hidden files):

```bash
$ du -h -a *
```

You can also use the `ls` command to list the files in any given directory (`-h` is again for human-readable, and `-a` is again to view all files, including hidden files):

```bash
$ ls -h -a *
```

# Valgrind Reports Memory Leak with `make gprof`
If your code was timing out because the runtime was too long, you likely investigated the runtime of the parts of your code using `gprof` (which is excellent!), and in doing so, you likely compiled your code using `make gprof`, which adds the `-pg` compilation flag to the compilation command (the `-pg` compilation flag is required in order to use `gprof`).

However, for reasons out-of-scope of this class, Valgrind doesn't play nicely with the `-pg` flag, and it will (potentially) incorrectly report a memory leak even if your code doesn't actually have a memory leak. Because of this, you will want to remove the `-pg` flag from your compilation command before checking for memory leaks (and before submitting your code, as the grader will be checking for memory leaks). For more information about Valgrind and `-pg`, see [this post](https://stackoverflow.com/a/14565503/2134991).

# Code Works on Example Datasets but Fails Grader
The small example datasets we provide are by no means exhaustive, nor are they intended to be. If your code seems to be working correctly on all of the example datasets we provide but fails the grader, that means that there is a bug in your code that needs to be fixed, and the only way to find the bug is to **design your own test datasets** to try to cover any corner cases you can think of in order to trigger the bug. The ability to design appropriate test datasets is one of the intended learning outcomes of this assignment.
