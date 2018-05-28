#coding=utf-8
import subprocess
import time
import logging
import ConfigParser

# 定期检查磁盘空间，如果磁盘空间使用率超过一定值，那么就清除指定文件

# 读取配置文件，设置全局基本配置
cf = ConfigParser.ConfigParser()
cf.read('./config')

# global variables
# log日志文件所在的位置
log_file = cf.get('log', 'log_file')
# log日志的输出level
log_level = getattr(logging, cf.get('log', 'log_level'), 'INFO')
# 定时清理的时间，cron表达式
clean_cron = cf.get('base', 'clean_cron')
# 触发磁盘空间清理行动的阀值，以“占用磁盘空间大小/总磁盘空间大小”来计算
disk_use_threshold = cf.getfloat('base', 'disk_use_threshold')

# 清理的文件名匹配的正则表达式
file_name_regexp = cf.get('file', 'file_name_regexp')
# 清理的文件的超期时间
file_expires = cf.getint('file', 'file_expires')

# basic config
logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# local variables
fail_times = 0

# script

print "------"
