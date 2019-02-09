#!/usr/bin/env python

"""
各种中间件装饰器
"""

import sys
import json
import time
import threading
import traceback
import pika
import paho.mqtt.client as mqtt
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
        except Exception:
            raise
        finally:
            G.getInstance().close()

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

        class Heartbeat(threading.Thread):
            def __init__(self, connection):
                super(Heartbeat, self).__init__()
                self.lock = threading.Lock()
                self.connection = connection
                self.quitflag = False
                self.stopflag = True
                self.setDaemon(True)

            def run(self):
                while not self.quitflag:
                    time.sleep(10)
                    self.lock.acquire()
                    if self.stopflag:
                        self.lock.release()
                        continue
                    try:
                        self.connection.process_data_events()
                    except Exception as ex:
                        self.lock.release()
                        return
                    self.lock.release()

            def startHeartbeat(self):
                self.lock.acquire()
                if self.quitflag == True:
                    self.lock.release()
                    return
                self.stopflag = False
                self.lock.release()

        heartbeat = Heartbeat(connection)
        heartbeat.start()
        heartbeat.startHeartbeat()

    return outer


def mqttWorkerFactory(hostname='', port=0, username='', password='', topic='#'):
    """ mqtt 工厂方法 """

    def outer(func):
        print("开始连接mqtt协议...")

        # connection mq

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            client.subscribe(topic)

        @TimeExpense
        def _deco(client, userdata, msg):
            try:
                print("\n" + Utils.currentTime() + " 开始执行业务方法")
                func(client, userdata, msg)
            except Exception as e:
                print("业务方法异常")

        client = mqtt.Client()
        client.reinitialise(client_id="xxx", clean_session=False, userdata=None)
        client.on_connect = on_connect
        client.on_message = _deco

        try:
            client.username_pw_set(username=username, password=password)
            client.connect(hostname, port, 60)
            client.loop_forever()
        except Exception as ex:
            raise ex
            print("mqtt服务异常")

    return outer
