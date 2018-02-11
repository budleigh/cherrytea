import datetime

import pytz

from cherrytea_app.models import DonationPlan, Donation
from cherrytea_app.logger import Logger


def run():
    # plans should be fulfilled if:
    # - today is the day of week they're created for localized to
    # - the timezone of the user they're attached to. for safety,
    # - we explicitly exclude those that have been fulfilled in
    # - the last 72 hours.
    today = datetime.datetime.now()
    logger = Logger()

    plans = DonationPlan.objects.all()  # todo filter properly or parallelize
    for plan in plans:
        timezone = pytz.timezone(plan.user.options.timezone)
        localized = timezone.localize(today)
        if localized.weekday() == today.weekday() and plan.last_fulfilled < (today - datetime.timedelta(hours=72)):
            try:
                donate(plan)
            except BaseException as e:
                logger.error('Failed to fulfill donation plan: %s' % e, plan)


def donate(plan):
    Donation.objects.create(
        group=plan.group,
        amount=plan.amount,
        user=plan.user,
        date=datetime.date.today(),
    )

    plan.last_fulfilled = datetime.datetime.now()
    plan.total_donated += plan.amount
    plan.save()


if __name__ == '__main__':
    run()
