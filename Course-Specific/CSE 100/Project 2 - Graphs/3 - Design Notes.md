Before you write even a single line of code, it's important to properly design the various components of your `Graph` class. Here, we will discuss some aspects of the design that you should be sure to think about.

# Parsing a CSV File
The edge list your `Graph` constructor needs to read will be a CSV file, such as the following CSV file with 3 columns:

```
Niema,Moshiri,100
Ryan,Micallef,95
Felix,Garcia,95
```

In C++, you can parse a CSV file as follows (note that `first`, `second`, and `third` are all `string` objects):

```cpp
ifstream my_file(filename);      // open the file
string line;                     // helper var to store current line
while(getline(my_file, line)) {  // read one line from the file
    istringstream ss(line);      // create istringstream of current line
    string first, second, third; // helper vars
    getline(ss, first, ',');     // store first column in "first"
    getline(ss, second, ',');    // store second column in "second"
    getline(ss, third, '\n');    // store third column column in "third"
}
my_file.close();                 // close file when done
```

* Don't forget to add `#include <fstream>` to the top of your code to be able to use `ifstream`!
    * Be sure to refer to the [`ifstream` C++ documentation](http://www.cplusplus.com/reference/fstream/ifstream/) for more information
* Don't forget to add `#include <sstream>` to the top of your code to be able to use `istringstream`!
    * Be sure to refer to the [`istringstream` C++ documentation](http://www.cplusplus.com/reference/sstream/istringstream/) for more information

# Using the C++ `tuple` Class
In order to represent the mathematical concept of a [tuple](https://en.wikipedia.org/wiki/Tuple), C++ provides a `tuple` class. Be sure to thoroughly read the [C++ `tuple` documentation](http://www.cplusplus.com/reference/tuple/tuple/), but the following code example will hopefully show you how to use it:

```cpp
#include <iostream> // load cout
#include <string>   // load string class
#include <tuple>    // load tuple class
using namespace std;
int main() {
    tuple<string,string,int> prof = make_tuple("Niema","Moshiri",1993);
    cout << "First Name: " << get<0>(prof) << endl;
    cout << "Last Name:  " << get<1>(prof) << endl;
    cout << "Birth Year: " << get<2>(prof) << endl;
}
```

You may or may not want to use `tuple` objects in your underlying `Graph` design, but you will likely want to use them as you implement the member functions of the `Graph` class (e.g. as you implement a graph traversal algorithm). Pro-tip: if you try to sort a `vector` that contains `tuple` objects using `std::sort`, the `tuple` objects will be sorted based on the first element.

# Using the C++ `pair` Class
Much like the `tuple` class, C++ provides the `pair` class that can be used to represent a pair of objects. Be sure to thoroughly read the [C++ `pair` documentation](http://www.cplusplus.com/reference/utility/pair/pair/), but the following code example will hopefully show you how to use it:

```cpp
#include <iostream> // load cout
#include <string>   // load string class
#include <utility>  // load pair class
using namespace std;
int main() {
    pair<string,string> prof = make_pair("Niema","Moshiri");
    cout << "First Name: " << prof.first << endl;
    cout << "Last Name:  " << prof.second << endl;
}
```

# Creating a C++ `struct`
When examining your data types, you may find yourself adding many properties to your `tuple` objects, or may want increased readability by creating custom types. C++ provides the ability to define a `struct`, which is essentially a simple class that can be used to bundle together elements. Be sure to thoroughly read the [C++ `struct` documentation](http://www.cplusplus.com/doc/tutorial/structures/), but the following code example will hopefully show you how to use it:

```cpp
#include <iostream> // load cout
#include <string>   // load string class
using namespace std;

// define struct
struct person {
    string first;
    string last;
    unsigned int year;
};

int main() {
    // create struct object on stack
    person prof = {
        .first = "Niema",
        .last  = "Moshiri",
        .year  = 1993
    };

    // access values of struct object to print
    cout << "First Name: " << prof.first << endl;
    cout << "Last Name:  " << prof.last << endl;
    cout << "Year:       " << prof.year << endl << endl;
    
    // change a value of the struct object
    prof.first = "Niemster";
    cout << "First Name: " << prof.first << endl;
    cout << "Last Name:  " << prof.last << endl;
    cout << "Year:       " << prof.year << endl << endl;

    // create struct object dynamically on heap
    person* prof_ptr = new person {
        .first = "Niema",
        .last  = "Moshiri",
        .year  = 1993
    };

    // access values of struct object to print
    cout << "First Name: " << prof_ptr->first << endl;
    cout << "Last Name:  " << prof_ptr->last << endl;
    cout << "Year:       " << prof_ptr->year << endl;
}
```

# Using a Custom Comparison Class with `priority_queue`
When you implement Dijkstra's Algorithm, you will likely want to store `tuple` objects representing (*total path weight*, *from*, *to*) tuples to keep track of your graph traversal. In C++, you can create a `priority_queue` with a custom comparison class. You may want to create a custom comparison class to compare these tuples in a way that uses the `priority_queue` as a min-heap with respect to total path weight. Be sure to read the [C++ `priority_queue` documentation](http://www.cplusplus.com/reference/queue/priority_queue/priority_queue/) thoroughly to see how to define a custom comparison class and use it with a `priority_queue` object.

# Modifying the `Makefile`
As you design your `Graph` class, you may feel as though you want to create additional code files for any helper classes you may potentially create. Note that you don't have to: you can complete this project without creating any additional files. However, if you do choose to do so, you will find that you will want to modify the `Makefile` in order to properly compile your executable. Feel free to make any modifications you wish, and you may want to refer to [this guide](https://docs.redhat.com/en/documentation/red_hat_developer_toolset/9/html/user_guide/chap-make) or [this tutorial](https://makefiletutorial.com/) to help you.
