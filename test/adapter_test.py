# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

def test_connection_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.connection()

def test_execute_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.execute('')

def test_tables_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.tables()

def test_columns_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.columns('')

def test_indexes_raises_error(db_adapter):
    with pytest.raises(NotImplementedError):
        db_adapter.indexes('')
