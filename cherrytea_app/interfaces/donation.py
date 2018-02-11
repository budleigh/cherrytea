from cherrytea_app.interfaces.base import BaseInterface
from cherrytea_app.models import Donation


class PlanInterface(BaseInterface):
    model = Donation
