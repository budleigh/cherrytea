from django.db import IntegrityError

from cherrytea_app.interfaces.base import BaseInterface, AccessError
from cherrytea_app.models import DonationPlan
from cherrytea_app.util import day_map


class PlanInterface(BaseInterface):
    model = DonationPlan

    def create(self, user, group, amount, day_of_week):
        for plan in user.plans.all():
            if plan.group == group:
                self.logger.error('plan creation clash', user, group)
                raise IntegrityError('plan for group already exists')

        return DonationPlan.objects.create(
            group=group,
            user=user,
            amount=amount,
            day=day_map[day_of_week],
        )

    def cancel(self, plan_id, user):
        plan = DonationPlan.objects.get(pk=plan_id)

        # this shouldnt be possible but yeah
        if plan.user != user:
            raise AccessError('plan not associated with user')

        self.logger.info('cancelling plan for user', plan, user)
        plan.delete()
