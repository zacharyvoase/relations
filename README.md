# Relations

Relations is a simple Python implementation of a relational algebra engine.


## Example

Create a relation with a heading (i.e. a list of field names):

    >>> import relations
    >>> employees = relations.Relation('employee_name', 'dept_name')
    >>> employees
    <Relation('dept_name', 'employee_name')>

The fields are re-ordered alphabetically, so that the order of values in tuples
is consistent between equivalent but separate relations. Add tuples to the
relation:

    >>> alice = employees.add(employee_name='Alice', dept_name='Finance')
    >>> bob = employees.add(employee_name='Bob', dept_name='Sales')
    >>> len(employees)
    2

A relation is a set; duplicate tuples are considered identical:

    >>> _ = employees.add(employee_name='Alice', dept_name='Finance')
    >>> len(employees)
    2

A relation implements the relational algebra, including the unary operators
**Select**:

    >>> finance_emps = employees.select(lambda emp: emp.dept_name == 'Finance')
    >>> len(finance_emps)
    1

**Project**:

    >>> names = employees.project('employee_name')
    >>> names.contains(employee_name='Bob')
    True
    >>> names.contains(employee_name='Charlie')
    False

and **Rename**:

    >>> employees_renamed = employees.rename(name='employee_name')
    >>> employees_renamed.contains(name='Bob')
    True

It also supports the set operations **Union**, **Intersection** and
**Difference**.


## Coming Soon

Joins:

* Natural join
* Theta join
* Equijoin
* Semijoin
* Antijoin
* Divide
* Left outer join
* Right outer join
* Full outer join


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
