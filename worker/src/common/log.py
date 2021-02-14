# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      logging
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import logging

# 初始化日志收集器
log = logging.getLogger('PowerJob')
log.setLevel("INFO")

# TODO: file logging
# 初始化日志处理器 - 文件输出（指定位置使用绝对路径，默认当前目录下）
# file_name = os.path.expanduser('~/powerjob/worker/logs/worker.log')
# file_handler = logging.FileHandler(file_name, encoding='utf-8')
# file_handler.setLevel("INFO")

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel("INFO")

# log.addHandler(file_handler)
log.addHandler(console_handler)

# 设置日志格式，中间间隔使用冒号也可以(模块名字-报错行-收集器名字-级别-信息)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)