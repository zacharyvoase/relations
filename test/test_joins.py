import relations


employees = relations.Relation('name', 'emp_id', 'dept_name')
employees.add(name='Harry', emp_id=3415, dept_name='Finance')
employees.add(name='Sally', emp_id=2241, dept_name='Sales')
employees.add(name='George', emp_id=3401, dept_name='Finance')
employees.add(name='Harriet', emp_id=2202, dept_name='Sales')

departments = relations.Relation('dept_name', 'manager')
departments.add(dept_name='Finance', manager='George')
departments.add(dept_name='Sales', manager='Harriet')
departments.add(dept_name='Production', manager='Charles')


def test_natural_join():
    joined = employees.natural_join(departments)

    assert len(joined) == 4


def test_natural_join_on_disjoint_relations_is_cartesian_product():
    joined = employees.project('name', 'emp_id').natural_join(departments)

    assert len(joined) == (len(employees) * len(departments))
