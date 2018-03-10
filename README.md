这是一个基于python3.5的脚本开发脚手架，集成了mysql(sqlalchemy), rabbitmq(pika), redis(redis)等常用的中间件，快速开发业务。
具体的使用方法见 controllers 目录下的 Test.py 文件

**配置环境**  
此脚手架使用openstack的 oslo.config 作为配置管理，目前区分三个环境，分别是线上环境(conf)，开发环境(debug)，预览环境(pre)。 指定环境有三种方式：

- 方式一：使用 --config-file=conf/xxx.ini 参数来读取指定配置。  
- 方式二：设置 UNITYMOB_ENVIRON 环境变量，变量值分别为 conf, debug, pre ，分别对应上述三个环境。  
- 方式三：如果不指定配置文件，也没有设置环境变量，则默认使用conf环境的配置。  
注意：如果同时设置了方式一和方式二，方式一的优先级级别最高。  

**使用方法**
- python3.5 cli.py --executer=test/get_all_user
- test_rabbitmq为一个rabbitmq 的worker端：python3.5 cli.py --executer=test/test_rabbitmq

- 同时也支持给方法传参数，方法如下：
python3.5 cli.py --executer=plan --args=one,two --kwargs=three:hello

**使用方法截图**
![Alt text](https://github.com/xiaowan/pyadmin/blob/master/snapshot/testcontroller.jpeg)
