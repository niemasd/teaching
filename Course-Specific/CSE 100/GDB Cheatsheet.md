Originally written by [Sravya Balasa](https://www.linkedin.com/in/sravyabalasa/)

# Q: What is GDB?
**GDB** is the **G**NU **D**e**b**ugger, a portable system that runs on many Unix-like systems. It is especially useful when debugging C/C++ programs, such as in CSE 100!

## Starting GDB
GDB takes in the name of your program's executable:

```bash
gdb ./QueueTest
```

## Breakpoints
* Breakpoints are one of GDB's most useful functionality!
* Breakpoints allow you to stop the execution of your program so you can go through each line step by step.
* The common practice is to set breakpoints ***before*** running your program. This allows your program to stop at a certain line when running it.

```
(b)reak filename:lineNumber
(b)reak filename:functionName
```

## Run
`run` or `r`

Runs your program until a breakpoint or finish.

However, if your executable takes in arguments, here is an alternative approach:

`r a1 a2 a3` runs your executable with `a1`, `a2`, and `a3` as the command-line arguments.

## Next
`next` or  `n`

Executes the next line of your program, displays the "next" line to be executed after that line.

## Step
`step` or  `s`

Steps into a function call. If there is no function call, executes the same functionality as `next`.

## Continue
`continue` or  `c`

Once your program is running, runs your program until the next breakpoint or until finish.

Note: Especially useful if you don't want to `next` or `step` your way through several recursive calls.

## Print
`print` or `p`

Prints the current values of variables in your program! Extremely useful debugging feature (: There are many variations of arguments to the command, use a search engine to see more.
* `print argv[i]`
* `print i`
* `print myPtr`	→ Prints the address `myPtr` holds
* `print *myPtr` → Prints the object `myPtr` is pointing to

You can also use one of these format specifiers, which allow you to see your output in non-decimal format if needed.
* `print i` → 2
* `print/t i` → 10

## Backtrace
`backtrace` or `bt`

Oh no! Your program segfaulted ): GDB has a command `backtrace` which prints out the stack trace from your program until failure.

This is especially useful to see which functions/lines your program went through before failure.

## Up
`up`

Travel up the function call stack by a single stack frame (i.e. a single function 
call)


# Notes
* `Ctrl-d` or `quit` exits the program
* GDB remembers the last command you executed, so you can repeatedly press `Enter` if you're executing the same command over and over.
* Here's a more comprehensive [cheatsheet](https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf) as well!
