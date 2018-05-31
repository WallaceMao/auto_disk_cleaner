#coding=utf-8
from crontab import CronTab

# script
cron = CronTab(user='root')
job = cron.new(command='python /root/python_space/rsq_file_cleaner/cleaner.py >> /var/log/rsq_file_cleaner.log 2>&1')
job.setall('*/1 * * * *')
#job.minute.every(1)
cron.write()
