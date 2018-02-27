这是一个基于python3.5的脚本开发脚手架，集成了mysql(sqlalchemy), rabbitmq, redis等常用的中间件，快速开发业务。

**demo**
- python3.5 cli.py --executer=test/get_all_user
- test_rabbitmq为一个rabbitmq 的worker端：python3.5 cli.py --executer=test/test_rabbitmq

- 同时也支持给方法传参数，方法如下：
python3.5 cli.py --executer=plan --args=one,two --kwargs=three:hello

