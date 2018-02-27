#!/usr/bin/env python

import os
import pika
import time
import pytz
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from mapper import UnitymobSession
from contextlib import contextmanager

from .MyRedis import MyRedis
from .MyRabbitmq import MyRabbitmq
from conf import conf


class Utils(object):
    @staticmethod
    def rabbitmqWorkerFactory(dsn='', exchange='', queue='', callback=None):
        # connection mq
        connection = pika.BlockingConnection(pika.URLParameters(dsn))
        channel = connection.channel()

        # declare exchange
        channel.exchange_declare(exchange=exchange, type='direct', durable=True)

        # declare queue
        result = channel.queue_declare(queue=queue, durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=exchange, queue=queue_name)

        # config for rabbitmq'worker
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue=queue, no_ack=False)

        channel.start_consuming()

    @staticmethod
    def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S%z'):
        local_format = "%Y-%m-%d %H:%M:%S"
        time_str = Utils.utc_to_str(utc_time_str=utc_time_str, utc_format=utc_format, local_format=local_format)
        return int(time.mktime(time.strptime(time_str, local_format)))

    @staticmethod
    def utc_to_str(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S%z', local_format="%Y-%m-%d %H:%M:%S"):
        local_tz = pytz.timezone('Asia/Chongqing')
        utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        time_str = local_dt.strftime(local_format)
        return time_str

    @staticmethod
    def theOtherDay(separation=1):
        """ 计算当前时间前几天的时间 """
        return datetime.date.today() + datetime.timedelta(days=separation)

    @staticmethod
    def strtimeToUTC(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S%z'):
        return datetime.datetime.strptime(utc_time_str, utc_format)

    @staticmethod
    def currentTime(format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format, time.localtime(int(time.time())))

    @staticmethod
    @contextmanager
    def rabbitmq():
        """ redis context """
        mq = MyRabbitmq(conf.rabbitmq.dsn)
        try:
            yield mq
        finally:
            mq.close()

    @staticmethod
    def getFileNameByPath(filePath):
        return os.path.split(filePath)[-1]

    @staticmethod
    def md5(str):
        m2 = hashlib.md5()
        m2.update("{str}".format(str=str).encode("utf-8"))
        return m2.hexdigest()

    @staticmethod
    def sendMail(title="", msg="", receiver=[]):
        """
        发送邮件
        :param title: 标题
        :param msg: 邮件内容
        :param receiver: 列表 所有邮件接受者
        :return: void
        """
        email = conf.email
        try:
            message = MIMEText(msg, 'plain', 'utf-8')
            message['from'] = email.user
            message['to'] = ';'.join(receiver)
            message['subject'] = Header(title, 'utf-8')

            smtp = smtplib.SMTP_SSL(email.host, email.port)
            smtp.set_debuglevel(0)
            smtp.login(email.user, email.password)
            smtp.sendmail(email.user, receiver, message.as_string())
            smtp.close()
        except Exception as e:
            print("报警邮件发送异常,生无可恋...")

    @staticmethod
    def debug(data):
        print(" ================== start debug ================== ")
        print(data)
        print(" ================== end debug ================== ")
        exit()
