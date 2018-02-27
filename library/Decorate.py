#!/usr/bin/env python

"""
工具类装饰器
"""

import sys
import time
from conf import log

from sqlalchemy.orm.session import Session
from mapper import UnitymobSession


def DI(**kwargs):
    """ 注入装饰 """

    def outer(cls):
        for x in kwargs:
            setattr(cls, x, kwargs.get(x))
        return cls

    return outer


def TimeExpense(func):
    """ 统计 job 执行时长 """

    def _deco(*args, **kwargs):
        start = int(time.time())
        func(*args, **kwargs)
        end = int(time.time())
        log.info("脚本运行结束,共计耗时 : {expense} 秒".format(expense=end - start))
        sys.stdout.flush()

    return _deco


def Transaction(name=None):
    """
    声明式事务,该方法只能使用在对方法上
    特性 :
        a. 支持直接传入session对象(暂无实现)
        b. 传入session对象对应的类书属性名称
    如果出现exception ,直接上抛异常给调用方
    """

    def outer(func):
        def _deco(self, *args, **kwargs):
            if name is not None and hasattr(self, name):
                session = getattr(self, name)
                if isinstance(session, Session):
                    try:
                        res = func(self, *args, **kwargs)
                        session.commit()
                        return res
                    except Exception as e:
                        session.rollback()
                        raise e
                    finally:
                        pass

        return _deco

    return outer


def session_init():
    def outer(func):
        def _deco(self, *args, **kwargs):
            try:
                session = UnitymobSession()
                setattr(self, 'session', session)
                res = func(self, *args, **kwargs)
                return res
            except Exception as e:
                raise e
            finally:
                session.close()

        return _deco

    return outer
