import urecord


class RelationalError(Exception):
    """Something attempted to perform an undefined or invalid operation."""
    pass


class Relation(object):

    def __init__(self, *fields):
        self.heading = frozenset(fields)
        self.tuple = urecord.Record(*fields)
        # Mapping of tuples => ids.
        self.tuples = {}
        # Mapping of ids => tuples.
        self.index = {}

    def clone(self):
        """Create a new, empty relation with the same heading as this one."""

        return type(self)(*self.tuple._fields)

    def add(self, *args, **kwargs):

        """
        Add a tuple to this relation.

        This method attempts to be as efficient as possible, re-using the same
        Python object if the tuple already exists in this relation.

        Arguments are given in either positional or keyword form:

            >>> employees = Relation('name', 'department')
            >>> alice = employees.add(name='Alice', department='Finance')
            >>> bob = employees.add('Bob', 'Sales')
        """

        tuple = self.tuple(*args, **kwargs)
        if tuple in self.tuples:
            return self.index[self.tuples[tuple]]
        self.tuples[tuple] = id(tuple)
        self.index[id(tuple)] = tuple
        return tuple

    def __len__(self):
        return len(self.tuples)

    def __contains__(self, tuple):
        return tuple in self.tuples

    def __iter__(self):
        pass

    def contains(self, *args, **kwargs):

        """
        Determine if this relation contains the specified tuple.

        Arguments are given in the same form as for :meth:`add`. This is easier
        than having to construct a tuple and use Python's `in` operator, e.g.:

            >>> employees.contains(name='Alice', department='Sales')
            True

        Whereas without this method you'd do:

            >>> employees.tuple(name='Alice', department='Sales') in employees
            True
        """

        tuple = self.tuple(*args, **kwargs)
        return tuple in self

    def select(self, predicate):

        """
        Filter the tuples in this relation based on a predicate.

        Returns a new, union-compatible relation.
        """

        new_relation = self.clone()
        for tuple in filter(predicate, self.tuples):
            new_relation.add(*tuple)
        return new_relation

    def project(self, *fields):

        """
        Return a new relation with a heading restricted to the given fields.

        The new relation is not union-compatible, and will also be a set, so
        it may have a smaller cardinality than the original relation. Here's
        an example:

            >>> employees = Relation('name', 'department')
            >>> employees.add(name='Alice', department='Sales')
            >>> employees.add(name='Bob', department='Sales')
            >>> len(employees)
            2
            >>> departments = employees.project('department')
            >>> len(departments)
            1
            >>> departments.contains(department='Sales')
            True
        """

        new_relation = type(self)(*fields)
        if not new_relation.heading.issubset(self.heading):
            undefined_fields = tuple(new_relation.heading.difference(self.heading))
            raise RelationalError("Undefined fields used in project(): %r" %
                                  undefined_fields)

        # Example: given the relation ('a', 'b', 'c') and fields ('a', 'c'),
        # indices will have a value of (0, 2).
        indices = map(self.tuple._fields.index, fields)
        # Continued:
        # project_one((a='foo', b='bar', c='baz')) => ('foo', 'baz')
        project_one = lambda t: map(t.__getitem__, indices)

        for tuple in self.tuples:
            new_relation.add(*project_one(tuple))
        return new_relation

    def rename(self, **new_fields):

        """
        Rename some fields in this relation.

        Accepts keyword arguments in the form
        ``new_field_name='old_field_name'``. The new relation returned will
        only be union-compatible if no arguments are given to this function.
        """

        if not is_bijection(new_fields):
            raise RelationalError("Field mapping is not one-to-one")
        elif not set(new_fields.values()).issubset(self.heading):
            undefined_fields = tuple(set(new_fields.values).difference(self.heading))
            raise RelationalError("Undefined fields used in rename(): %r" %
                                  undefined_fields)

        # Mapping from old field name => new field name.
        rename = invert_bijection(new_fields)

        new_relation = type(self)(*map(lambda f: rename.get(f, f),
                                       self.tuple._fields))
        for tuple in self.tuples:
            new_relation.add(*tuple)
        return new_relation


def is_bijection(dictionary):
    """Check if a dictionary is a proper one-to-one mapping."""

    return len(set(dictionary.keys())) == len(set(dictionary.values()))


def invert_bijection(dictionary):
    """Return the inverse of a bijection. Does not check the input."""

    return dict((value, key) for (key, value) in dictionary.iteritems())
