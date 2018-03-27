#!/usr/bin/env python3.5

from conf import conf
from .Base import BaseController
from models.Test import TestModel
from library.Middleware import rabbitmqWorkerFactory, Clear, TimeExpense
import time


class TestController(BaseController):
    # 该属性为默认执行该类的业务处理方法
    default_method = 'get_all_user'

    def __init__(self):
        self.testModel = TestModel.getInstance()
        super().__init__()

    def prepare(self):
        print("先于执行业务方法执行的逻辑")

    @Clear
    def get_all_user(self):
        users = self.testModel.get_all_user()
        for user in users:
            print(user.nickname + '---' + user.loginname)

    def test_rabbitmq(self):
        @rabbitmqWorkerFactory(conf.rabbitmq.dsn, 'exchange_name', 'queue_name')
        def consum_mq(ch, method, properties, body):
            """ 在这里处理队列信息 """
            print(body)

    @TimeExpense
    def test_time_expense(self):
        time.sleep(3)

