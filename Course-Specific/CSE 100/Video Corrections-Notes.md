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
