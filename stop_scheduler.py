#coding=utf-8
from crontab import CronTab

# script
cron = CronTab(user='root')
cron.remove_all()
cron.write()
