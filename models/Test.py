#!/usr/bin/env python3.5

from .Base import BaseModel
from mapper.UserDO import UserDO


class TestModel(BaseModel):
    def get_all_user(self):
        return self.session.query(UserDO).all()



