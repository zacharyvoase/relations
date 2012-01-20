from nose.tools import assert_raises

import relations


def test_equivalent_relations_are_union_compatible():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('gender', 'age', 'name')
    assert rel1.is_union_compatible(rel2)


def test_unequivalent_relations_are_union_compatible():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('symbol', 'price')
    assert not rel1.is_union_compatible(rel2)


def test_union_contains_elements_from_both_relations():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('gender', 'age', 'name')
    rel1.add(name='Alice', age=25, gender='F')
    rel2.add(name='Bob', age=32, gender='M')

    union = rel1.union(rel2)
    assert union.contains(name='Alice', age=25, gender='F')
    assert union.contains(name='Bob', age=32, gender='M')


def test_set_operations_raise_error_if_not_union_compatible():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('symbol', 'price')
    rel1.add(name='Alice', age=25, gender='F')
    rel2.add(symbol='AAPL', price='424.47')

    assert_raises(relations.NotUnionCompatible,
                  lambda: rel1.union(rel2))
    assert_raises(relations.NotUnionCompatible,
                  lambda: rel1.intersection(rel2))
    assert_raises(relations.NotUnionCompatible,
                  lambda: rel1.difference(rel2))


def test_intersection_contains_only_elements_present_in_both_relations():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('gender', 'age', 'name')
    rel1.add(name='Alice', age=25, gender='F')
    rel1.add(name='Bob', age=32, gender='M')
    rel1.add(name='Charlie', age=65, gender='M')
    rel2.add(name='Bob', age=32, gender='M')
    rel2.add(name='Charlie', age=65, gender='M')

    intersection = rel1.intersection(rel2)
    assert len(intersection) == 2
    assert not intersection.contains(name='Alice', age=25, gender='F')


def test_difference_contains_elements_present_in_self_but_not_in_other():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('gender', 'age', 'name')
    rel1.add(name='Alice', age=25, gender='F')
    rel1.add(name='Bob', age=32, gender='M')
    rel1.add(name='Charlie', age=65, gender='M')
    rel2.add(name='Bob', age=32, gender='M')
    rel2.add(name='Charlie', age=65, gender='M')

    diff = rel1.difference(rel2)
    assert len(diff) == 1
    assert diff.contains(name='Alice', age=25, gender='F')
