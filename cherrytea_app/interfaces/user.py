import stripe

from cherrytea_app.interfaces.base import BaseInterface, AccessError
from cherrytea_app.models import User, UserOptions

stripe.api_key = ''


class UserInterface(BaseInterface):
    model = User

    def _create_stripe_user(self, user):
        customer = stripe.Customer.create(
            email=user.email,
        )
        user.options.stripe_id = customer.id
        user.options.save()

    def create_user(self, email, password, timezone='US/Pacific'):
        user = User.objects.create_user(username=email, email=email, password=password)
        UserOptions.objects.create(user=user, timezone=timezone)
        self._create_stripe_user(user)
        return user
