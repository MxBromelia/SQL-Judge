""" A Mock for a Database Adapter, used to run tests """
from typing import List, Dict, Tuple
from .adapter import AbstractAdapter

FILTER_OUT_TABLE_PARAMS = {'triggers', 'columns'}
FILTER_OUT_COLUMN_PARAMS = {'indexes', 'constraints', 'primary_key', 'references'}

class SerializedAdapter(AbstractAdapter):
    """Adapter to a generated serialized schema, that is generated by the validator.
    The Serialized version can be exported to a text file in JSON format and used as caching
    (Not yet implemented)"""
    def __init__(self, info: dict):
        self._info = info

    def tables(self) -> List[Dict[str, str]]:
        return [
            {'name': table, **{k: v for k, v in params.items() if k not in FILTER_OUT_TABLE_PARAMS}}
            for table, params in self._info.get('tables', {}).items()
        ]

    def _table_cols(self):
        for table, table_params in self._info.get('tables', {}).items():
            for column, column_params in table_params.get('columns', {}).items():
                yield table, column, column_params

    def columns(self) -> List[Dict[str, str]]:
        columns_info = []
        for table, column, column_params in self._table_cols():
            params = {k: v for k, v in column_params.items() if k not in FILTER_OUT_COLUMN_PARAMS}
            columns_info.append({'table': table, 'name': column, **params})
        return columns_info

    def primary_keys(self) -> List[Tuple[str,str]]:
        primary_keys = []
        for table, column, params in self._table_cols():
            if params.get('primary_key') is True:
                primary_keys.append((table, column))
        return primary_keys

    def references(self) -> List[Dict[str, str]]:
        references = []
        for table, column, params in self._table_cols():
            refs = params.get('references')
            if refs is not None:
                references.append({'table': table, 'column': column, 'references': refs})
        return references

    def indexes(self) -> List[Dict[str, str]]:
        indexes = []
        for table, column, params in self._table_cols():
            for index, index_params in params.get('indexes', {}).items():
                indexes.append({'table': table, 'column': column, 'name': index, **index_params})
        return indexes

    def constraints(self) -> List[Dict[str, str]]:
        constraints = []
        for table, column, params in self._table_cols():
            for constraint, cons_params in params.get('constraints', {}).items():
                constraints.append({'table': table, 'column': column, 'name': constraint, **cons_params})
        return constraints

    def triggers(self) -> List[Dict[str, str]]:
        triggers = []
        for table, params in self._info.get('tables', {}).items():
            for trigger, trigger_params in params.get('triggers', {}).items():
                triggers.append({'table': table, 'name': trigger, **trigger_params})
        return triggers

    def _entities(self, group):
        return [{'name': entity, **params} for entity, params in self._info.get(group, {}).items()]

    def functions(self) -> List[Dict[str, str]]:
        return self._entities('functions')

    def procedures(self) -> List[Dict[str, str]]:
        return self._entities('procedures')

    def sequences(self) -> List[Dict[str, str]]:
        return self._entities('sequences')
