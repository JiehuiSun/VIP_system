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