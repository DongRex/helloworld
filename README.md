# 使用方法

前端提交 ->  插入数据库 -> python读取数据库定时每日一报  （默认使用requests 每日一报 可自行修改为 chromewebdriver）



请自行配置数据库 加密采用AES128位加密  不需要可以关闭加密



关于work.py 中 basekey 如何获取 

1. 在提交的时候按f12 图1
2. 提交 然后选中刚才提交的找到F_state 就是basekey 内容 图2和图3



liunx 下定时任务

crontab -e
