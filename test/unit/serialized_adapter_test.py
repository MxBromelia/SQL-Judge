# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

@pytest.fixture
def adapter(build_schema_adapter):
    return build_schema_adapter({
        'tables': {
            'table_one': {
                'columns': {
                    'column_one': {
                        'type': 'int', 'primary_key': True, 'constraints': {
                            'column_one_constraint': {'type': 'primary_key'},
                            'column_one_constraint_2': {'type': 'not null'}
                    }}, 'column_two': {'type': 'int', 'references': 'table_two'}
                }, 'triggers': {
                    'trigger_one': {'hook': 'hook_one'}
                }
            }, 'table_two': {
                'columns': {
                    'column_three': {
                        'type': 'int', 'primary_key': True,
                        'indexes': {'column_three_index': {}}
                    },
                    'column_four': {'type': 'int'}
                }, 'triggers': {
                    'trigger_two': {'hook': 'hook_two'}
                }
            }
        }
    })

#pylint: disable=redefined-outer-name
def test_adapter_cannot_call_the_same_method_twice(adapter):
    with pytest.raises(AttributeError):
        adapter.tables()
        adapter.tables()

def test_mock_adapter_tables(adapter):
    assert adapter.tables() == [{'name': 'table_one'}, {'name': 'table_two'}]

def test_columns(adapter):
    assert adapter.columns() == [
        {'table_name': 'table_one', 'name': 'column_one', 'type': 'int'},
        {'table_name': 'table_one', 'name': 'column_two', 'type': 'int'},
        {'table_name': 'table_two', 'name': 'column_three', 'type': 'int'},
        {'table_name': 'table_two', 'name': 'column_four', 'type': 'int'}
    ]

def test_primary_key(adapter):
    assert adapter.primary_keys() == [
        ('table_one', 'column_one'),
        ('table_two', 'column_three')
    ]

def test_no_primary_key(build_schema_adapter):
    no_pkey = build_schema_adapter({'tables': {'table_one': {'columns': {'column_one': {}}}}})
    assert no_pkey.primary_keys() == []

def test_references(adapter):
    assert adapter.references() == [
        ('table_one', 'column_two', 'table_two')
    ]

def test_indexes(adapter):
    assert adapter.indexes() == [
        {'table_name': 'table_two', 'column_name': 'column_three', 'name': 'column_three_index'}
    ]

def test_constraints(adapter):
    assert adapter.constraints() == [
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'column_one_constraint', 'type': 'primary_key'},
        {'table_name': 'table_one', 'column_name': 'column_one', 'name': 'column_one_constraint_2', 'type': 'not null'}
    ]

def test_triggers(adapter):
    assert adapter.triggers() == [
        {'table_name': 'table_one', 'name': 'trigger_one', 'hook': 'hook_one'},
        {'table_name': 'table_two', 'name': 'trigger_two', 'hook': 'hook_two'}
    ]

def test_functions(build_schema_adapter):
    assert build_schema_adapter({'functions': {'function_one': {}}}).functions() == [{'name': 'function_one'}]

def test_procedures(build_schema_adapter):
    assert build_schema_adapter({'procedures': {'procedure_one': {}}}).procedures() == [{'name': 'procedure_one'}]
