from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'date', run_date = date(2021, 11, 30))
    scheduler.add_job(job, 'date', run_date = datetime(2021, 11, 30, 1, 0, 0))
    scheduler.add_job(job, 'date', run_date = '2021-11-30 01:00:00')
    scheduler.add_job(job, 'interval', minutes = 1)
    scheduler.add_job(job, 'interval', minutes = 1, seconds = 30, start_date = '2019-08-29 22:15:00', end_date = '2019-08-29 22:17:00')
    scheduler.add_job(job, 'cron', day_of_week = '0-4', hour = '10, 16', minute = '50')
    scheduler.start()


def job():
    print('test')


if __name__ == '__main__':
    main()

    
# https://www.cnblogs.com/gdjlc/p/11432526.html
