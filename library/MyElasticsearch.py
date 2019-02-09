#!/usr/bin/env python


from elasticsearch import Elasticsearch


class MyElasticsearch(object):
    """ elasticsearch 连接 """
    _instance = None

    def __init__(self, dsn=None):
        self.dsn = dsn if isinstance(dsn, list) else [dsn]
        self._client = None

    @classmethod
    def getInstance(cls, dsn=None):
        if cls._instance is None:
            cls._instance = cls(dsn=dsn)
        return cls._instance

    @property
    def get_es_client(self):
        if self._client is None:
            self._client = Elasticsearch(self.dsn)
        return self._client
