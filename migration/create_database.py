# -*- coding: UTF-8 -*-

from os.path import isfile
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.models import Base, SettingsTable, UsersTable
from application.shared.log import create_logger
from config import IPP, DB_FILE, DB_URI


def create_database():
    """Creates SQLite database and populates it with example data"""
    logger = create_logger(__file__)
    if isfile(DB_FILE):
        logger.info("SQLite database already exists at '{}'".format(DB_FILE))
    else:
        logger.info("Creating SQLite database at '{}' ...".format(DB_FILE))
        db_session = None
        try:
            engine = create_engine(DB_URI)
            Base.metadata.create_all(engine)
            DBSession = sessionmaker(bind=engine)
            db_session = DBSession()
            # Add user
            user = UsersTable(
                username="demo",
                password="pbkdf2:sha256:150000$O8FkuFnd$aeaf19d0b50d4862f1c9b770441685d5f78335fc111916a1ffef915a266b2e92",
                api_key="pbkdf2:sha256:150000$ReI2eIGn$a4f6920eb66c6a5518ab9c58739b67348bf2f45bebd5cc3cbf106daf053ae53f"
            )
            db_session.add(user)
            # Add setting
            setting = SettingsTable(
                items_per_page=IPP
            )
            db_session.add(setting)
            db_session.commit()
            db_session.close()
        except Exception:
            logger.error("Failed to create valid SQLite database!", exc_info=True)
        finally:
            if db_session is not None:
                db_session.close()
    logger.info("Done.")


if __name__ == "__main__":
    sys.exit(create_database())
