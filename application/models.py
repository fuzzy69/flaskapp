# -*- coding: UTF-8 -*-

from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.dialects.mysql import INTEGER
import tables

from config import IPP


Base = declarative_base()


class BaseTable(Base):
    """Base table model"""
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class UsersTable(BaseTable):
    """Users table model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    api_key = Column(String(128))


class SettingsTable(BaseTable):
    """Settings table model"""
    __tablename__ = "settings"

    items_per_page = Column(INTEGER, nullable=False, default=IPP)


class OXTS(tables.IsDescription):
    """"""
    timestamp    = tables.StringCol(32)
    lat          = tables.Float64Col()
    lon          = tables.Float64Col()
    alt          = tables.Float64Col()
    roll         = tables.Float64Col()
    pitch        = tables.Float64Col()
    yaw          = tables.Float64Col()
    vn           = tables.Float64Col()
    ve           = tables.Float64Col()
    vf           = tables.Float64Col()
    vl           = tables.Float64Col()
    vu           = tables.Float64Col()
    ax           = tables.Float64Col()
    ay           = tables.Float64Col()
    az           = tables.Float64Col()
    af           = tables.Float64Col()
    al           = tables.Float64Col()
    au           = tables.Float64Col()
    wx           = tables.Float64Col()
    wy           = tables.Float64Col()
    wz           = tables.Float64Col()
    wf           = tables.Float64Col()
    wl           = tables.Float64Col()
    wu           = tables.Float64Col()
    pos_accuracy = tables.Float64Col()
    vel_accuracy = tables.Float64Col()
    navstat      = tables.UInt8Col()
    numsats      = tables.UInt8Col()
    posmode      = tables.UInt8Col()
    velmode      = tables.UInt8Col()
    orimode      = tables.UInt8Col()


