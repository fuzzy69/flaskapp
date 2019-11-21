# -*- coding: UTF-8 -*-

from os.path import isfile

import tables

from application.errors import DataError
from config import IPP, H5_FILE, OXTS_TABLE_COLUMNS


class DataFile:
    """HFS5 file context manager"""

    def __init__(self, file_path: str):
        """
        :param str file_path: file path to h5 data file
        """
        self._file_path = file_path
        self._h5_file = None

    def __enter__(self):
        """Overridden"""
        self._h5_file = tables.open_file(self._file_path, mode='r')
        return self._h5_file

    def __exit__(self, *args):
        """Overridden"""
        self._h5_file.close()


class DataTable:
    """Simple wrapper for reading H5 files thorough PyTables"""

    def __init__(self, data_file: str):
        """
        :param str data_file: file path to h5 data file
        """
        self._data_file = data_file
        self._rows_count = 0

    @property
    def rows_count(self) -> int:
        """Returns number of result rows"""
        return self._rows_count

    def fetch_rows(self, start: int=0, stop: int=IPP, **filters):
        """Yield all rows from table in selected start/stop range"""
        try:
            with DataFile(self._data_file) as h5file:
                table = h5file.root.sequences.oxts
                self._rows_count = int(table.shape[0])
                query = []
                if filters:
                    # TODO: filter type checking and sanitization
                    for k, v in filters.items():
                        if k in OXTS_TABLE_COLUMNS:
                            if isinstance(v, (int, float)):
                                query.append("({} == {})".format(k, v))
                            else:
                                query.append("({} == '{}')".format(k, v))
                    if len(query) > 0:
                        query = ' & '.join(query)
                if query:
                    for row in table.where(query):
                        yield row
                else:
                    for row in table.iterrows(start, stop):
                        yield row
        except:
            raise DataError("Failed to query KITTI data file!")

    def fetch_rows_as_tuples(self, start: int=0, stop: int=IPP, **filters):
        """"Yield all rows as tuples from table in selected start/stop range"""
        for row in self.fetch_rows(start, stop, **filters):
            yield tuple(row[attr].decode("utf-8") if attr == "timestamp" else row[attr]
                        for attr in OXTS_TABLE_COLUMNS)

    def fetch_rows_as_dicts(self, start: int=0, stop: int=IPP, **filters):
        """"Yield all rows as tuples from table in selected start/stop range"""
        for row in self.fetch_rows(start, stop, **filters):
            yield {attr: row[attr].decode("utf-8") if attr == "timestamp" else row[attr]
                        for attr in OXTS_TABLE_COLUMNS}
