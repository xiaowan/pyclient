#!/usr/bin/env python

from conf import conf
from library.G import G
from contextlib import closing


class Execute(object):

    def __init__(self):
        self._executor = None
        self._method = None
        self._analyze_executor(conf.executer)
        self._args = conf.args
        self._kwargs = conf.kwargs

    def _analyze_executor(self, invoker):
        """ 分析执行者 """
        _invoker = invoker.split('/', 1)
        if len(_invoker) == 1:
            self._executor = _invoker[0]

        if len(_invoker) == 2:
            self._executor = _invoker[0]
            self._method = _invoker[1]

    def run(self):
        """ 开始执行 """
        invoker_prefix = str(self._executor).capitalize()
        controller = "{invoker}Controller".format(invoker=invoker_prefix)

        executor = __import__("controllers.{invoker}".format(invoker=invoker_prefix), fromlist=controller)
        executor_obj = eval("executor.{controller}.getInstance()".format(controller=controller))

        if self._method is None:
            if hasattr(executor_obj, 'default_method'):
                self._method = executor_obj.default_method.lower()

        try:
            method = getattr(executor_obj, self._method)
            method(*self._args, **self._kwargs)
        except Exception:
            raise
        finally:
            if not G.getInstance().is_cleard:
                with closing(G.getInstance()):
                    pass


def main():
    try:
        Execute().run()
        return 0
    except Exception as ex:
        print(ex)
    finally:
        return 1

