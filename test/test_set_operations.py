import relations


def test_equivalent_relations_are_union_compatible():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('gender', 'age', 'name')
    assert rel1.is_union_compatible(rel2)


def test_unequivalent_relations_are_union_compatible():
    rel1 = relations.Relation('name', 'age', 'gender')
    rel2 = relations.Relation('symbol', 'price')
    assert not rel1.is_union_compatible(rel2)
