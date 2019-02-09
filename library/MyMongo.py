#!/usr/bin/env python

from pymongo import MongoClient


class MyMongo(object):
    """ mongodb 连接 """

    _instance = None

    def __init__(self, dsn=None):
        self.dsn = dsn
        self._mongodb_client = None

    @classmethod
    def getInstance(cls, dsn=None):
        if cls._instance is None:
            cls._instance = cls(dsn=dsn)
        return cls._instance

    def close(self):
        if self._mongodb_client is not None:
            self._mongodb_client.close()

    @property
    def get_mongodb_client(self):
        if self._mongodb_client is None:
            self._mongodb_client = MongoClient(self.dsn)
        return self._mongodb_client
