# VIP_system
制作会员系统

操作系统：Ubuntu 16.04 server 64bit  
python版本: 3.6.5  
Flask版本: 1.0.2  
Redis版本: 4.0.9  
Mysql版本: 5.7.22  

一、错误类型定义
---
> 每个项目中都有自己的错误定义及处理，并且是属于基础功能，因此先了解错误类型定义

具体讲解请查看文件: ```vip_system/errors.py```

二、Session处理
---
> 和移动端交互一般都采用token来进行认证，web也可以这样操作
> 这里自己定义Session的存储，将token存入redis

具体讲解请查看文件:```utils/session.py```

三、Redis使用
---
> 项目中很多使用缓存的地方，因此需要使用redis

具体讲解请查看文件: ```utils/flask_redis.py```

四、Flask配置
---
> 配置文件一般都会因为环境不同，而值不同，因此需要能区分出不同环境。
> 1. 可以指定配置文件位置
> 2. 可以使用系统环境变量来赋值
> 3. 使用import文件覆盖当前配置，也就是这里使用的方法

具体讲解请查看文件: ```vip_system/configs.py```

五、工具功能
---
> 项目中有很多工具功能需要编写，所以统一都写在utils下，这里先写一个时间转换功能
> 几乎所有项目都会有时间转换的需求

具体讲解请查看文件: ```utils/time_utils.py```

六、业务功能模块
---
> 根据项目的实际情况来划分不同业务模块，以独立的目录形式存在
> 目录下分models.py、urls.py、views.py、controllers.py
> 比如用户模块独立创建一个目录account
> 在account/models.py中增加User类

七、基础接口类定义
---
> 定义接口基础类，所以其它接口实现都需要继承此类，统一进行认证、异常、返回数据等操作

具体讲解请查看文件```api/__init__.py```

八、实现具体的一个接口
---
> 实现一个最基础的登录接口，来演示controller、views、urls、model之间的相互关系

具体讲解请分别查看文件:
```account/controllers.py```
```account/views.py```
```account/urls.py```

九、应用实例
---
> 配置启用的app实例，其实日志文件放在项目根目录下的var/log下，此目录会自动创建

具体讲解请查看文件: ```application.py```

十、数据库管理
---
> 使用alembic进行数据库的管理
> 1. pip install alembic 进行安装
> 2. 在项目目录下执行 ```alembic init migrations```，此时项目目录会生成alembic.ini文件，在里面配置自己的mysql：sqlalchemy.url
> 3. 修改```migrations/env.py```文件内容：target_metadata
> 4. 将项目根目录写入环境变量PYTHONPATH: ```export PYTHONPATH=$PYTHONPATH```:你的项目目录路径
> 5. 此时执行：```alembic revision --autogenerate -m "create user table"```，这样就会在migrations/versions中生成数据库迁移文件
> 6. 执行：```alembic upgrade head```，就会在你的数据库中生成user表
> 注意：请先在你的mysql中创建相应的数据库

十一、通过flask_script运行服务
---
> 目前基本的功能可以使用了，那么就需要运行起来服务进行测试
> 使用flask_script来完成

具体讲解请查看文件: ```manage.py```
