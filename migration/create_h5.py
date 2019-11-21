# -*- coding: UTF-8 -*-

from os.path import join
from pathlib import Path
import sys

import pykitti
import tables

from application.models import OXTS
from application.shared.log import create_logger
from config import OXTS_TABLE_COLUMNS, ROOT_DIR, H5_FILE


DATASET_DIR = join(Path(ROOT_DIR).parent, "dataset")
DATE = "2011_10_03"
DRIVE = "0042"
logger = create_logger(__file__)


def import_oxts():
    """Imports OXTS data to a HFS5 file"""
    logger.info("Importing OXTS data to {} ...".format(H5_FILE))
    dataset = pykitti.raw(DATASET_DIR, DATE, DRIVE, frames=range(0, 1170))
    # PyTables
    h5file = tables.open_file(H5_FILE, mode="w", title="KITTI")
    group = h5file.create_group("/", "sequences", "Sequences")
    table = h5file.create_table(group, "oxts", OXTS, "OXTS")
    row = table.row
    for i, oxt in enumerate(dataset.oxts):
        row["timestamp"] = dataset.timestamps[i]
        for attr in OXTS_TABLE_COLUMNS[1:]:
            row[attr] =  getattr(oxt.packet, attr)
        row.append()
    table.flush()


def import_velo():
    """Imports Velodyne data from KITTI data set to HFS5 file"""
    logger.info("Importing Velodyne data to {} ...".format(H5_FILE))
    # TODO: Finish this
    # dataset = pykitti.raw(DATASET_DIR, DATE, DRIVE, frames=range(0, 10))
    # return

    # v = np.asarray(dataset.velo)
    # v = [v for velo in dataset.velo
    #         for v in velo]
    # print(type(v))
    #
    # pprint(v, indent=4)
    # return
    # np.savetxt(VELO_CSV_FILE, np.asarray(dataset.velo), delimiter=",")
    # for i, velo in enumerate(dataset.velo):
    #     for j, v in enumerate(velo):
    #         print(type(v))
    #         pprint(v)
    #         x, y, z, reflectance = v
    #         print(j, x, y, z, reflectance)
            # break
        # break


def main() -> int:
    """Script main entry point"""
    logger.info("Importing KITTI data set ...")
    try:
        import_oxts()
        import_velo()
    except Exception:
        logger.error("Failed to import all data to H5 file '{}'!".format(H5_FILE), exc_info=True)
    logger.info("Done.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
