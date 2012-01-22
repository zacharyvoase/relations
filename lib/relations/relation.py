import functools
from itertools import imap

import urecord

from relations.tuple import Tuple


__all__ = ['Relation', 'RelationalError', 'UndefinedFields',
           'NotUnionCompatible']


class RelationalError(Exception):
    """An undefined or invalid operation was attempted."""
    pass


class UndefinedFields(RelationalError):
    """An undefined field was used in an operation on one or more relations."""
    pass


class NotUnionCompatible(RelationalError):
    """A set operation was attempted between non-union-compatible relations."""
    pass


def check_union_compatible(method):
    @functools.wraps(method)
    def wrapper(self, other):
        if not self.is_union_compatible(other):
            raise NotUnionCompatible
        return method(self, other)
    return wrapper


class Relation(object):

    def __init__(self, *fields, **kwargs):
        self.heading = frozenset(fields)
        self.tuple = urecord.Record(*sorted(fields), instance=Tuple)
        self.tuples = {}

    def __repr__(self):
        return '<Relation%r>' % (self.tuple._fields,)

    def __len__(self):
        return len(self.tuples)

    def __contains__(self, tuple_):
        return tuple_ in self.tuples

    def __iter__(self):
        return iter(self.tuples)

    def clone(self):
        """Create a new, empty relation with the same heading as this one."""

        return type(self)(*self.tuple._fields)

    def is_union_compatible(self, other):
        return self.heading == other.heading

    @check_union_compatible
    def update(self, other):

        """
        Merge this relation with another union-compatible relation.

        This method modifies (and returns) this relation. The other relation
        is not modified.
        """

        self.tuples.update(other.tuples)
        return self

    @check_union_compatible
    def union(self, other):
        """Safe set union between two union-compatible relations."""

        return self.clone().update(self).update(other)

    @check_union_compatible
    def intersection(self, other):
        """Safe set intersection between two union-compatible relations."""

        new_relation = self.clone()
        new_relation.tuples.update(
            (tuple_, tuple_) for tuple_ in
                set(self.tuples).intersection(set(other.tuples)))
        return new_relation

    @check_union_compatible
    def difference(self, other):
        """Safe set difference between two union-compatible relations."""

        new_relation = self.clone()
        new_relation.tuples.update(
            (tuple_, tuple_) for tuple_ in
                set(self.tuples).difference(set(other.tuples)))
        return new_relation

    def add(self, **kwargs):

        """
        Add a tuple to this relation.

        This method attempts to be as efficient as possible, re-using the same
        Python object if the tuple already exists in this relation.

        Arguments should be given in keyword form:

            >>> employees = Relation('name', 'department')
            >>> alice = employees.add(name='Alice', department='Finance')
            >>> alice.name
            'Alice'
            >>> alice.department
            'Finance'
        """

        tuple_ = self.tuple(**kwargs)
        return self.tuples.setdefault(tuple_, tuple_)

    def contains(self, **kwargs):

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

        return self.tuple(**kwargs) in self

    def select(self, predicate):

        """
        Filter the tuples in this relation based on a predicate.

        Returns a new, union-compatible relation.
        """

        new_relation = self.clone()
        new_relation.tuples.update(
            (tuple_, tuple_) for tuple_ in filter(predicate, self.tuples))
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
            raise UndefinedFields("Undefined fields used in project(): %r" %
                                  undefined_fields)

        projection = self.tuple._make_projection(*fields)

        new_relation.tuples.update((tuple_, tuple_)
            for tuple_ in imap(
                lambda t: new_relation.tuple(*t._index_restrict(*projection)),
                self.tuples))
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
            undefined_fields = tuple(set(new_fields.values()).difference(self.heading))
            raise UndefinedFields("Undefined fields used in rename(): %r" %
                                  undefined_fields)

        # Get a complete bijection from new field names => old field names
        renamed_fields = set(new_fields.values())
        for field_name in self.heading:
            if field_name not in renamed_fields:
                new_fields[field_name] = field_name

        new_relation = type(self)(*new_fields.keys())
        reordering = self.tuple._make_reordering(**new_fields)
        new_relation.tuples.update(
            (tuple_, tuple_) for tuple_ in imap(
                lambda t: new_relation.tuple(*t._index_restrict(*reordering)),
                self.tuples))
        return new_relation

    def natural_join(self, other):
        new_relation = type(self)(*self.heading.union(other.heading))
        common_fields = self.heading.intersection(other.heading)
        projection1 = self.tuple._make_projection(*common_fields)
        projection2 = other.tuple._make_projection(*common_fields)
        for tuple1 in self:
            for tuple2 in other:
                if (tuple1._index_restrict(*projection1) ==
                    tuple2._index_restrict(*projection2)):
                    row = tuple1._asdict()
                    row.update(tuple2._asdict())
                    new_relation.add(**row)
        return new_relation


def is_bijection(dictionary):
    """Check if a dictionary is a proper one-to-one mapping."""

    return len(set(dictionary.keys())) == len(set(dictionary.values()))


def invert_bijection(dictionary):
    """Return the inverse of a bijection. Does not check the input."""

    return dict((value, key) for (key, value) in dictionary.iteritems())
