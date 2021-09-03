
from flask import Flask
from flask_apscheduler import APScheduler

class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'task1', # 任务id
            'func': '__main__:task', # 任务执行程序
            #'args': None, # 执行程序参数
            #'trigger': 'interval', # 任务执行类型，定时器
            #'seconds': 5, # 任务执行时间，单位秒
            'trigger': {
                'type': 'cron',  # 类型
                'second': '*/3'  # "*/3" 表示每3秒执行一次，单独一个"3" 表示每分钟的3秒。
            }
        }
    ]

def task():
    print('test')

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(SchedulerConfig())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run()

'''
interval 触发器 
参数 说明 
weeks (int) 间隔几周 
days (int) 间隔几天 
hours (int) 间隔几小时 
minutes (int) 间隔几分钟 
seconds (int) 间隔多少秒 
start_date (datetime 或 str) 开始日期 
end_date (datetime 或 str) 结束日期 

cron 触发器: 
参数 说明 
year (int 或 str) 年，4位数字 
month (int 或 str) 月 (范围1-12) 
day (int 或 str) 日 (范围1-31 
week (int 或 str) 周 (范围1-53) 
day_of_week (int 或 str) 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun) 
hour (int 或 str) 时 (范围0-23) 
minute (int 或 str) 分 (范围0-59) 
second (int 或 str) 秒 (范围0-59) 
start_date (datetime 或 str) 最早开始日期(包含) 
end_date (datetime 或 str) 最晚结束时间(包含) 
'''
