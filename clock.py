import django
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

from cherrytea_app.jobs.fulfill_plans import run as fulfill_plans
from cherrytea_app.logger import Logger

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=1)
def run_fulfill_plans_job():
    logger = Logger()
    logger.info('starting fulfill_plans job')
    try:
        fulfill_plans()
    except BaseException as e:
        logger.error('error running fulfill_plans job: %s' % e)
    logger.info('completed fulfill_plans job')


sched.start()
