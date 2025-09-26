As you work on this Project, you will almost certainly run into bugs you will need to find and fix. Here, we will provide some general tips for debugging that may prove useful.

# Designing and Drawing Out Graphs
Be sure to design your own graph CSV files to test your code, and be sure to actually manually draw out exactly what the graphs look like and exactly how the various graph algorithms should execute on your graphs. Try to think of corner cases you might face and how your code should handle them. When we say that you should "draw out" the graph, we mean **literally draw it out by hand!** Whether you prefer to draw it out using pen and paper, or on your tablet, or using your mouse or touchpad with Microsoft Paint, or using Zoom's whiteboard feature while you're having a video chat with your parents and want to show them all the amazing things you're learning in CSE 100, *please* actually draw out your test graphs and actually step through the graph algorithms by hand!

# JSON Pretty Print
The `GraphTest` executable will generally print 2 tab-delimited columns: a descriptor (left) followed by a JSON-formatted output produced by running your code. It outputs the JSON output in a compact manner that may be difficult for you to read as you try to debug your code. Instead of trying to read the JSON output in this compact manner, you can copy it and paste it into a JSON [pretty printer](https://en.wikipedia.org/wiki/Prettyprint), which will reformat it to make it easier to read. There are numerous online tools that do this, with one nice option being [JSON Formatter](https://jsonformatter.org/). For example, you can copy the following compact JSON:

```json
{"first":"Niema","last":"Moshiri","year":1993}
```

You can then paste this into the left text box on JSON Formatter and click the "Format/Beautify" button. Once you click this button, you should see the "beautified" version of the JSON in the right text box:

```json
{
  "first": "Niema",
  "last": "Moshiri",
  "year": 1993
}
```

Because `GraphTest` was actually designed to output in a format that would be easily parseable by Python, some outputs (e.g. the output of `Neighbors` in the `graph_properties` test) are actually not valid JSON (even though they are valid Python syntax). If you try using JSON Formatter and it gives you a syntax error, try using [Python Formatter](https://codebeautify.org/python-formatter-beautifier).

# Comparing JSON Files
When debugging, it may be useful to use a program to compare your code's JSON output to the known correct output to make sure it's correct. Since JSON's key-pair values may be stored in any order (similarly to a hash map), using regular `diff` or comparing by hand may prove difficult. You may use whatever you like, but [JSON Diff](http://www.jsondiff.com/) is one useful tool for performing such comparisons:
1. First, paste the known correct JSON output into the box on the left
2. Then, paste your code's JSON output into the box on the right
3. Remove any extra newline characters that may be in either box
4. Click the "Compare" button, which will display the two JSONs side-by-side and show the differences (if any)
    * If there *are* any differences, rows highlighted in blue represent values that differ, and rows highlighted in green represent missing (or extra!) key-value pairs
    * If there *are not* any differences (i.e., the JSONs were identical), it will display the following text: "The two files were semantically identical."

# Using `gdb` to Help You Debug
As you implement your `Graph` class, you will want to be able to debug effectively. Be sure to make use of `gdb` (the **G**NU **D**e**b**ugger) to help you step through your code, print variables, etc. You can refer to [this cheat sheet](https://github.com/niemasd/teaching/blob/master/Course-Specific/CSE%20100/GDB%20Cheatsheet.md) to help you use `gdb` if you don't remember how. If your code is producing the incorrect problem on a specific graph, try physically drawing out the graph and manually stepping through the graph algorithm while simultaneously stepping through your code line-by-line using `gdb`, printing variables as needed, in order to pinpoint where and how exactly your code diverges from your logic.

# Speeding Up Code
If your code is taking too long to run, you will want to investigate *which parts* of your code are slow so you can speed up those specific parts. On pretty much any Linux platform, you can use `gprof` (**G**NU **Prof**iler) to perform "per-function profiling". There are more complicated profiling tools that exist, so if you feel comfortable learning how to set up / use one of those, feel free, but `gprof` works for me. The basic workflow is as follows:

```bash
$ make gprof             # Step 1: Compile your program with the -pg flag (we provide a Makefile target for convenience)
$ ./my_exe               # Step 2: Run your program (it will create a file gmon.out)
$ gprof my_exe | less -S # Step 3: Run gprof to profile (I pipe to less -S to make it easier to read)
```

The `gprof` output tells you what percentage of your runtime was spent on each function that was called in your code. Note that the profiling results will likely be uninformative on small datasets because the overall runtime will be too small, so you will want to design larger test datasets of your own to get more meaningful profiling results. Many times, the runtime will be some built-in C++ STL function, so you may think "Well, that's not my code, so that's not something I can speed up", but that would be incorrect! If a built-in C++ STL function is taking a bunch of runtime, it's because *you're calling* that function :-) So try to find where in your code you're calling it a bunch of times, and try to refactor that part of your code! Feel free to refer to [this lengthier tutorial about `gprof`](https://www.thegeekstuff.com/2012/08/gprof-tutorial/).
