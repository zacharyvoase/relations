from nose.tools import assert_raises

import relations


def test_a_relation_has_a_heading():
    employees = relations.Relation('employee_name', 'dept_name')
    assert employees.heading == set(['employee_name', 'dept_name'])


def test_a_relation_has_cardinality():
    employees = relations.Relation('employee_name', 'dept_name')
    assert len(employees) == 0
    employees.add(employee_name='Alice', dept_name='Finance')
    assert len(employees) == 1


def test_a_relation_has_membership():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    assert employees.contains(employee_name='Alice', dept_name='Finance')
    assert not employees.contains(employee_name='Bob', dept_name='Sales')


def test_a_relation_has_a_tuple():
    employees = relations.Relation('employee_name', 'dept_name')
    emp = employees.tuple(employee_name='Alice', dept_name='Finance')
    assert emp.employee_name == 'Alice'
    assert emp.dept_name == 'Finance'


def test_a_relation_is_a_set():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Alice', dept_name='Finance')
    assert len(employees) == 1
    employees.add(employee_name='Bob', dept_name='Sales')
    assert len(employees) == 2


def test_select_creates_a_new_relation_with_the_same_heading():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Bob', dept_name='Sales')

    selected = employees.select(lambda emp: emp.dept_name == 'Finance')
    assert isinstance(selected, relations.Relation)
    assert selected.heading == employees.heading


def test_project_creates_a_new_relation():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Bob', dept_name='Sales')

    names = employees.project('employee_name')
    assert isinstance(names, relations.Relation)
    assert names.heading == set(['employee_name'])
    assert names.contains(employee_name='Alice')
    assert names.contains(employee_name='Bob')
    assert len(names) == 2


def test_project_raises_error_on_undefined_fields():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Bob', dept_name='Sales')

    assert_raises(relations.UndefinedFields,
                  lambda: employees.project('foobar'))


def test_projected_relations_are_sets():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Bob', dept_name='Finance')

    departments = employees.project('dept_name')
    assert departments.contains(dept_name='Finance')
    assert len(departments) == 1


def test_rename_creates_a_new_relation():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Bob', dept_name='Sales')

    new_emps = employees.rename(name='employee_name', dept='dept_name')
    assert new_emps.contains(name='Alice', dept='Finance')
    assert new_emps.contains(name='Bob', dept='Sales')


def test_rename_raises_error_on_undefined_fields():
    employees = relations.Relation('employee_name', 'dept_name')
    employees.add(employee_name='Alice', dept_name='Finance')
    employees.add(employee_name='Bob', dept_name='Sales')

    assert_raises(relations.UndefinedFields,
                  lambda: employees.rename(newfield='foobar'))
