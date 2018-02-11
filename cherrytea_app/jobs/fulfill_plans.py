import datetime

import pytz
import stripe

from cherrytea_app.models import DonationPlan, Donation
from cherrytea_app.logger import Logger
from cherrytea_app.interfaces import DonationInterface

stripe.api_key = 'sk_test_3PFwtSlitXPqUhUmFXWi7sbR'


def run():
    # plans should be fulfilled if:
    # - today is the day of week they're created for localized to
    # - the timezone of the user they're attached to. for safety,
    # - we explicitly exclude those that have been fulfilled in
    # - the last 72 hours.
    today = datetime.datetime.now()
    logger = Logger()
    donation_interface = DonationInterface()

    plans = DonationPlan.objects.all()  # todo filter properly or parallelize
    for plan in plans:
        timezone = pytz.timezone(plan.user.options.timezone)
        localized = timezone.localize(today)
        if localized.weekday() == today.weekday() and plan.last_fulfilled < (today - datetime.timedelta(hours=72)):
            try:
                donation_interface.donate(plan)
            except BaseException as e:
                logger.error('Failed to fulfill donation plan: %s' % e, plan)


if __name__ == '__main__':
    run()
