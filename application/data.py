
from os.path import isfile

from pandas import DataFrame, read_csv
import tables

from application.errors import DataError
from config import IPP, H5_FILE, OXTS_CSV_FILE, OXTS_TABLE_COLUMNS


def get_oxts(start: int=0, stop: int=IPP) -> tuple:
    """"""
    rows = []
    total_rows_count = 0
    if isfile(H5_FILE):
        h5file = None
        try:
            h5file = tables.open_file(H5_FILE, mode="r")
            table = h5file.root.sequences.oxts
            total_rows_count = int(table.shape[0])
            rows = [tuple(row[attr].decode("utf-8") if attr == "timestamp" else row[attr]
                        for attr in OXTS_TABLE_COLUMNS)
                            for row in table.iterrows(start, stop)]
        except:
            raise DataError("Failed to query KITTI data file!")
        finally:
            if h5file is not None:
                h5file.close()

    return rows, total_rows_count


def get_oxts_as_dicts(start: int=0, stop: int=IPP) -> tuple:
    """"""
    rows = []
    total_rows_count = 0
    if isfile(H5_FILE):
        h5file = None
        try:
            h5file = tables.open_file(H5_FILE, mode="r")
            table = h5file.root.sequences.oxts
            total_rows_count = int(table.shape[0])
            rows = [{attr: row[attr].decode("utf-8") if attr == "timestamp" else row[attr]
                        for attr in OXTS_TABLE_COLUMNS}
                            for row in table.iterrows(start, stop)]
        except:
            raise DataError("Failed to query KITTI data file!")
        finally:
            if h5file is not None:
                h5file.close()

    return rows, total_rows_count
