# easy_flask
用flask搭建最小可用框架，可以在此基础上进行开发

操作系统：Ubuntu 16.04 server 64bit  
python版本: 3.6.5  
Flask版本: 1.0.2  
Redis版本: 4.0.9  
Mysql版本: 5.7.22  

一、错误类型定义
---
> 每个项目中都有自己的错误定义及处理，并且是属于基础功能，因此先了解错误类型定义

具体讲解请查看文件: easy_flask/errors.py

二、Session处理
---
> 和移动端交互一般都采用token来进行认证，web也可以这样操作
> 这里自己定义Session的存储，将token存入redis

具体讲解请查看文件: utils/session.py

三、Redis使用
---
> 项目中很多使用缓存的地方，因此需要使用redis

具体讲解请查看文件: utils/flask_redis.py

四、Flask配置
---
> 配置文件一般都会因为环境不同，而值不同，因此需要能区分出不同环境。
> 1. 可以指定配置文件位置
> 2. 可以使用系统环境变量来赋值
> 3. 使用import文件覆盖当前配置，也就是这里使用的方法

具体讲解请查看文件: easy_flask/configs.py