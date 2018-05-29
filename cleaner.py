#coding=utf-8
import subprocess
import time
import logging
import ConfigParser
import os
import re
import datetime

# 定期检查磁盘空间，如果磁盘空间使用率超过一定值，那么就清除指定文件

# 读取配置文件，设置全局基本配置
cf = ConfigParser.ConfigParser()
cf.read('/etc/rsq_file_cleaner/config')

# global variables
# log日志文件所在的位置
log_file = cf.get('log', 'log_file')
# log日志的输出level
log_level = getattr(logging, cf.get('log', 'log_level'), 'INFO')
# 定时清理的时间，cron表达式
clean_cron = cf.get('base', 'clean_cron')
# 触发磁盘空间清理行动的阀值，以“占用磁盘空间大小/总磁盘空间大小”来计算
disk_use_threshold = cf.getfloat('base', 'disk_use_threshold')

file_search_path = cf.get('file', 'file_search_path')
# 清理的文件名匹配的正则表达式
file_name_regexp = cf.get('file', 'file_name_regexp')
# 清理的文件的超期时间
file_expires = cf.getint('file', 'file_expires')

# basic config
logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# local variables
fail_times = 0

# script
statvfs = os.statvfs('/')
usage_rate = 1 - statvfs.f_bavail / float(statvfs.f_blocks)
logging.info('disk usage checked, threshold is %s, current usage rate is %s' % (disk_use_threshold, usage_rate))

if usage_rate < disk_use_threshold:
  exit(0)

logging.info('begin to clean files')
time_limit = int(round(time.time())) - file_expires
logging.info('files modified before %s are going to be cleaned' % datetime.datetime.fromtimestamp(time_limit).strftime('%Y-%m-%d %H:%M:%S'))

for path in file_search_path.split(','):
  logging.info('--checking path %s for clean' % path)
  for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    stat = os.stat(filepath)
    if os.path.isfile(filepath) and re.match(file_name_regexp, filename) and int(stat.st_mtime) < time_limit:
      os.remove(filepath)
      logging.info('----file removed, path: %s, file: %s, mtime: %s' % (path, filename, datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')))
