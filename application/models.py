# -*- coding: UTF-8 -*-

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy.dialects.mysql import INTEGER
from tables import IsDescription, Float64Col, StringCol, UInt8Col

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


class OXTS(IsDescription):
    """HFS5 OXTS table model"""
    timestamp    = StringCol(32)
    lat          = Float64Col()
    lon          = Float64Col()
    alt          = Float64Col()
    roll         = Float64Col()
    pitch        = Float64Col()
    yaw          = Float64Col()
    vn           = Float64Col()
    ve           = Float64Col()
    vf           = Float64Col()
    vl           = Float64Col()
    vu           = Float64Col()
    ax           = Float64Col()
    ay           = Float64Col()
    az           = Float64Col()
    af           = Float64Col()
    al           = Float64Col()
    au           = Float64Col()
    wx           = Float64Col()
    wy           = Float64Col()
    wz           = Float64Col()
    wf           = Float64Col()
    wl           = Float64Col()
    wu           = Float64Col()
    pos_accuracy = Float64Col()
    vel_accuracy = Float64Col()
    navstat      = UInt8Col()
    numsats      = UInt8Col()
    posmode      = UInt8Col()
    velmode      = UInt8Col()
    orimode      = UInt8Col()
