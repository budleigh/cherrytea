from cherrytea_app.interfaces.base import BaseInterface
from cherrytea_app.models import CharityGroup


class GroupInterface(BaseInterface):
    model = CharityGroup
