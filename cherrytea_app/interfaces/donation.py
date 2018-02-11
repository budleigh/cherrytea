import datetime
from django.db import transaction

import stripe

from cherrytea_app.interfaces.base import BaseInterface
from cherrytea_app.models import Donation

stripe.api_key = ''


class DonationInterface(BaseInterface):
    model = Donation

    @transaction.atomic
    def donate(self, plan):
        # get the money here
        stripe.Charge.create(
            amount=plan.amount,
            currency="usd",
            description="Donation from %s for %s on %s (UTC)" % (
                plan.user.email,
                plan.group.name,
                datetime.date.today(),
            )
        )

        Donation.objects.create(
            group=plan.group,
            amount=plan.amount,
            user=plan.user,
            date=datetime.date.today(),
        )

        plan.last_fulfilled = datetime.datetime.now()
        plan.total_donated += plan.amount
        plan.save()
