geekpy.cn
======
Is Geekpy.cn Project. (geekpy.cn GeekPy-极客派项目）
The web site by django. ( 基于Django开发的网站 )


项目运行须知
------
1.  先安装requirements.txt中的依赖环境
2.  生成数据库迁移文件
3.  迁移数据库
4.  运行 post/tests.py 与 user/tests.py 脚本, 批量生成用户及文章
5.  开启 Redis 服务，如果 IP 端口非默认，则需在 GeekPy/settings.py 中配置。
6.  如果未安装 Redis, 则在 GeekPy/settings.py 中注释相关配置
