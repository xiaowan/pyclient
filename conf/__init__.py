#!/usr/bin/env python

from oslo_config import cfg
from oslo_log import log as logging
from os.path import join, dirname
from os import environ

conf = cfg.CONF
log = logging.getLogger(__name__)
logging.register_options(conf)

# common
default_opts = [
    cfg.StrOpt(name="environ", default="UNITYMOB_ENVIRON"),  # 环境变量key
    cfg.StrOpt(name="env", default="conf"),  # 环境变量key
    cfg.ListOpt(name="args", default=[]), #  外部位置参数
    cfg.DictOpt(name="kwargs", default={}), # 外部字典参数
    cfg.StrOpt(name="executer", default=None) # 逻辑执行者
]
conf.register_cli_opts(default_opts)

# sqlalchemy
sqlalchemy = cfg.OptGroup(name='sqlalchemy', title="MySQL ORM 相关配置")
conf.register_group(sqlalchemy)
conf.register_cli_opts([
    cfg.BoolOpt('echo', default=True),
    cfg.BoolOpt('autoflush', default=True),
    cfg.IntOpt('pool_size', 10),
    cfg.IntOpt('pool_recycle', 3600)
], sqlalchemy)

# email
email = cfg.OptGroup(name='email', title="邮件服务相关配置")
conf.register_group(email)
conf.register_cli_opts([
    cfg.StrOpt("host", default="smtp.mxhichina.com"),
    cfg.IntOpt("port", default=465),
    cfg.StrOpt("user", default="zybi@jollycorp.com"),
    cfg.StrOpt("password", default="jolly@2015")
], email)

# rabbitmq
rabbitmq = cfg.OptGroup(name='rabbitmq', title="RabbitMq 相关配置")
conf.register_group(rabbitmq)
conf.register_cli_opts([
    cfg.StrOpt('dsn', default=''),
], rabbitmq)

# mysql
mysql = cfg.OptGroup(name='mysql', title="MySQL DSN配置")
conf.register_group(mysql)
conf.register_cli_opts([
    cfg.StrOpt('unitymob', default='localhost'),
    cfg.StrOpt('jolly_brands', default='localhost'),
], mysql)

# facebook
facebook = cfg.OptGroup(name='facebook', title="FaceBook 相关配置")
conf.register_group(facebook)
conf.register_cli_opts([
    cfg.StrOpt('app_id', default=''),
    cfg.StrOpt('app_secret', default=''),
    cfg.StrOpt('access_token', default=''),
], facebook)

# redis
redis = cfg.OptGroup(name='redis', title="Redis 相关配置")
conf.register_group(redis)
conf.register_cli_opts([
    cfg.StrOpt('host', default='127.0.0.1'),
    cfg.IntOpt('port', default=6379),
    cfg.StrOpt('password', default='unitymob'),
], redis)

env = environ.get(conf.environ, 'conf')
env = env if env in ['debug', 'pre', 'conf'] else 'conf'
conf(default_config_files=[join(dirname(__file__), '.'.join([env, 'ini']))])

logging.setup(conf, "pyclient")