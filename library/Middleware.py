#!/usr/bin/env python

"""
各种中间件装饰器
"""

import sys
import json
import traceback
import pika
from oslo_context import context
from conf import conf, log
from library.Utils import Utils
from library.G import G
from library.Decorate import TimeExpense
from facebookads.api import FacebookAdsApi


def Clear(func):
    """ 负责清理中间遇到的所有资源问题，目前已经不使用 """

    def _deco(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            G.getInstance().clear()

    return _deco


def ApiInit(func):
    """ Facebook Api 初始化装饰器 """

    def _deco(*args, **kwargs):
        access_token = None
        try:
            body = json.loads(args[3].decode())
            access_token = body.get('access_token')
        except Exception as ex:
            access_token = conf.facebook.access_token

        finally:
            FacebookAdsApi.init(conf.facebook.app_id, conf.facebook.app_secret, access_token)
            func(*args, **kwargs)

    return _deco


def rabbitmqWorkerFactory(dsn='', exchange='', queue=''):
    """ rabbitmq """
    print("执行rabbitmq 预初始工作")

    def outer(func):
        print("开始连接rabbitmq")
        # connection mq
        connection = pika.BlockingConnection(pika.URLParameters(dsn))
        channel = connection.channel()

        # declare exchange
        channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)

        # declare queue
        result = channel.queue_declare(queue=queue, durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=exchange, queue=queue_name)

        # config for rabbitmq'worker
        channel.basic_qos(prefetch_count=1)

        @TimeExpense
        def _deco(ch, method, properties, body):
            try:
                context.RequestContext()
                log.info("开始执行业务方法")
                func(ch, method, properties, body)
            except Exception as e:
                print(e)
                if conf.env == 'conf':
                    mail_title = Utils.currentTime() + " " + sys.argv[0] + "执行异常,异常内容见邮件"
                    Utils.sendMail(mail_title, traceback.format_exc(), [
                        '邮箱地址'
                    ])
                else:
                    traceback.print_exc()
                log.info("业务方法异常")

            finally:
                log.info("队列消息确认消费")
                ch.basic_ack(delivery_tag=method.delivery_tag)

        sys.stdout.flush()
        channel.basic_consume(_deco, queue=queue, no_ack=False)

        channel.start_consuming()

    return outer
