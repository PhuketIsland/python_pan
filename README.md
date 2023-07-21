# python_pan

pan目录下是服务端代码
pan-client是客户端代码

默认使用IO+多线程的方式（在main.py中修改）：
from src.select_server import SelectServer  # IO方式
from src.threading_server import SelectServer  #IO+多线程

使用方法：
登录：login 用户名 密码
注册：register 用户名 密码
查看：ls 目录
上传：upload 本地目录 远程目录
下载：download 本地目录 远程目录 
