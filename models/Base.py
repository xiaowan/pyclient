#!/usr/bin/env python3.5

from library.Decorate import Transaction
from library.Classes import Classes


class BaseModel(Classes.BaseMinix):

    @Transaction(name="session")
    def save(self, obj):
        """ 保存对象，支持批量写入"""
        if isinstance(obj, list):
            res = self.session.add_all(obj)
        else:
            res = self.session.add(obj)
        self.session.flush()
        return res
