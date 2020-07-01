# add_table_to_schema
import pytest
from lib.schema_operations import add_column_to_table, add_table_to_schema, add_index_to_column

def test_no_schema_cannot_have_tables_added(table):
    with pytest.raises(TypeError):
        add_table_to_schema(None, table)

def test_cannot_add_no_table_to_a_schema(schema):
    with pytest.raises(TypeError):
        add_table_to_schema(schema, None)

def test_add_table_assigns_schema_to_table(schema, table):
    add_table_to_schema(schema, table)

    assert table.schema == schema

def test_add_table_adds_the_table_to_schema(schema, table):
    add_table_to_schema(schema, table)

    assert table in schema.tables

# add_column_to_table
def test_cannot_add_column_to_no_table(column):
    with pytest.raises(TypeError):
        add_column_to_table(None, column)

def test_cannot_add_no_column_to_table(table):
    with pytest.raises(TypeError):
        add_column_to_table(table, None)

def test_add_column_assigns_table_to_column(table, column):
    add_column_to_table(table, column)

    assert column.table == table

def test_add_column_adds_the_column_to_table(table, column):
    add_column_to_table(table, column)

    assert column in table.columns

def test_add_column_with_primary_key(table, primary_key_column):
    add_column_to_table(table=table, column=primary_key_column)

    assert table.primary_key == primary_key_column

def test_add_column_cannot_reassign_primary_key(table, build_column):
    column = build_column(primary_key=True)
    add_column_to_table(table=table, column=build_column(primary_key=True))

    assert add_column_to_table(table=table, column=column) is False
    assert column not in table.columns

# add_index_to_column
def test_cannot_add_index_to_no_column(column):
    with pytest.raises(TypeError):
        add_index_to_column(None, column)

def test_cannot_add_no_index_to_a_column(index):
    with pytest.raises(TypeError):
        add_index_to_column(index, None)

def test_add_index_assigns_column_to_index(column, index):
    add_index_to_column(column, index)

    assert column.index == index

def test_add_index_assigns_index_to_column(column, index):
    add_index_to_column(column, index)

    assert index.column == column
