#!/usr/bin/env python3.5

from . import BaseDO
from sqlalchemy import Column
from sqlalchemy.types import *


class UserDO(BaseDO):
    __tablename__ = 'py_user'

    nickname = Column(VARCHAR, default=None)
    loginname = Column(VARCHAR, default=None)
    avatar = Column(VARCHAR, default=None)
    is_valid = Column(VARCHAR, default=None)
