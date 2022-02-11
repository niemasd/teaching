# Video Corrections/Notes
These are corrections/notes for videos in my [*Advanced Data Structures*](https://www.youtube.com/playlist?list=PLM_KIlU0WoXmkV4QB1Dg8PtJaHTdWHwRS) YouTube playlist.

## [C++ Data Types — 3:55](https://youtu.be/HvMd5G_LAHE?t=235)
I say [`stringstream`](http://www.cplusplus.com/reference/sstream/stringstream/stringstream/), not "string string".

## [C++ Memory Diagrams — 2:05](https://youtu.be/Fv1PmkgQbeU?t=125)
Should be "And this `Student` object is called `s1`", not "And this [`string`](https://www.cplusplus.com/reference/string/string/) object is called `s1`".

## [AVL Rotations — 10:46](https://youtu.be/xzmLuS0ZJmA?t=646)
I accidentally said "right child of 8" and "left child of 5," but I meant to say "left child of 8" and "right child of 5" (which is what I correctly drew in the tree).

## [Proof of AVL Tree Worst-Case Time Complexity — 10:20](https://youtu.be/hUzRX1LzGXI?t=620)
I meant <sup>*h*</sup>/<sub>2</sub> (what I wrote), but I accidentally said "h minus 2" instead of "h over 2".

## [Proof of AVL Tree Worst-Case Time Complexity — 10:34](https://youtu.be/hUzRX1LzGXI?t=634)
To explain why *N<sub>h</sub>* is greater than 2<sup>*h*/2</sup>:
* Recall that *N<sub>h</sub>* is the minimum number of nodes in an AVL tree with height *h*
  * Therefore, *N*<sub>*h*-2</sub> is the minimum number of nodes in an AVL tree with height *h*-2
* In general, the maximum number of nodes in a binary tree with height *h* is roughly 2<sup>*h*</sup> (plus or minus 1 here or there depending on if you define height by edges or by nodes, but same general idea): it would be a perfectly balanced binary tree
  * Therefore, 2<sup>*h*/2</sup> is the maximum number of nodes in a binary tree with height <sup>*h*</sup>/<sub>2</sub>
* 2 times the minimum number of nodes in an AVL tree with height *h*-2 (i.e., 2*N*<sub>*h*-2</sub>) is larger than the maximum number of nodes in a (perfectly-balanced) binary tree with height <sup>*h*</sup>/<sub>2</sub> (which is 2<sup>*h*/2</sup>) (this may not be obvious, but try drawing it out with many examples)
* Therefore, if *N<sub>h</sub>* is greater than 2*N*<sub>*h*-2</sub> and 2*N*<sub>*h*-2</sub> is greater than 2<sup>*h*/2</sup>, then *N<sub>h</sub>* is greater than 2<sup>*h*/2</sup>

## [Proof of Red-Black Tree Worst-Case Time Complexity — 11:13](https://youtu.be/aRkE7DmVbCE?t=673)
Should be "equal to", not "greater than or equal to".

## [Implementing the Set and Map ADTs — 1:32](https://youtu.be/BbHf6N-DJRo?t=92)
O(1) insertion into an unsorted Linked List is only possible if we know in advance that we will not receive duplicate items. If we may receive duplicate items, we need to check for duplicates in insert to avoid unbounded time complexity in find and remove, which would make it O(*n*).

## [Implementing the Set and Map ADTs — 4:49](https://youtu.be/BbHf6N-DJRo?t=289)
O(1) amortized insertion into an unsorted Array List is only possible if we know in advance that we will not receive duplicate items. If we may receive duplicate items, we need to check for duplicates in insert to avoid unbounded time complexity in find and remove, which would make it O(*n*).

## [MWT Space Complexity — 8:37](https://youtu.be/e-Fie3g62H8?t=517)
|*∑*|<sup>*k*+1</sup> is the number of ***nodes*** in the MWT, not the number of pointers. Each node has |*∑*| pointers, so the total number of ***pointers*** would be |*∑*|<sup>*k*+2</sup>

## [TST Find — 2:43](https://youtu.be/mAOnwl3--wg?t=163)
The current node is actually **`n`**, not `i`. I should be comparing the current letter (`d`) against `n`.

## [The Birthday Paradox — 12:13](https://youtu.be/F57Xsl5WOXc?t=733)
The formula <sup>1</sup>/<sub>2</sub>(1 + <sup>1</sup>/<sub>1-*α*</sub>) is actually the "expected number of operations to find an element," NOT the "expected number of collisions".
* The two values are related, but they are ***not equal***
* You can find that derivation here if you're interested: http://cseweb.ucsd.edu/~kube/cls/100/Lectures/lec16/lec16-28.html#pgfId-980264

## [Double Hashing — 6:46](https://youtu.be/EEjdu-85fWQ?t=406)
*h*<sub>1</sub>(*k*) should be *h*<sub>1</sub>(*x*).

## [Bytewise I/O](https://youtu.be/txWMqAg6x08)
In my diagram, I have the input/output stream as a separate box as its corresponding buffer, but a better way to think about it is that the input/output stream has a buffer ***within*** it (i.e., the "buffer" box would be ***inside*** of the "input" or "output stream" box).

## [Bitwise I/O](https://youtu.be/nhMs1u9TGNo)
In my diagram, I have the input/output stream as a separate box as its corresponding buffer, but a better way to think about it is that the input/output stream has a buffer ***within*** it (i.e., the "buffer" box would be ***inside*** of the "input" or "output stream" box). Also, I have a bitwise buffer interact directly with memory and directly with an input/output stream, but a better way to draw it would be to have a "bitwise input stream" and "bitwise output stream" with a bitwise buffer ***within*** it.

## [Reading from a Bitwise Buffer — 2:14](https://youtu.be/FwPlWFzlgZo?t=134)
We are not actually done at `buf >> (7-c)`: this would get the "current" bit into the rightmost spot, but it would accidentally leave the bits to the left of the "current" bit in the number. We actually have to do `(buf >> (7-c)) & 1`, i.e., we have to then `AND` the result with 1 to extract just the rightmost bit.
