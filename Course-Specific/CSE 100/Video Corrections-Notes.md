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
