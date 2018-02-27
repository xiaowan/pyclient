#!/usr/bin/env python

__author__ = "yishan@jollycorp.com"

import redis

class MyRedis(object):
    """ redis config """

    _instance = None

    redis

    def __init__(self, host, port, password, decode_responses):
        self.redis = redis.StrictRedis(host=host, port=port, password=password, decode_responses=decode_responses)

    @classmethod
    def getInstance(cls, host, port, password, decode_responses):
        if cls._instance is None:
            cls._instance = cls(host, port, password, decode_responses)
        return cls._instance

    def get(self, key):
        return self.redis.get(key)

    def set(self, name, value):
        return self.redis.set(name, value)

    def incr(self, name, amount=1):
        return self.redis.incr(name, amount)

    def decr(self, name, amount=1):
        return self.redis.decr(name, amount)

    def keys(self, pattern='*'):
        return self.redis.keys(pattern='*')

    def delete(self, *names):
        return self.redis.delete(*names)

    def getPipe(self, transaction=True, shard_hint=None):
        return self.redis.pipeline(transaction=transaction, shard_hint=shard_hint)

    def close(self):
        """ 官方暂无实现 """
        pass