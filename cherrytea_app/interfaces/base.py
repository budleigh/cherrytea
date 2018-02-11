from cherrytea_app.logger import Logger


class AccessError(Exception):
    pass


class BaseInterface(object):
    model = None

    def __init__(self):
        self.logger = Logger()

    def all(self):
        return self.model.objects.all()

    def get(self, id):
        if not self.model:
            raise TypeError('model not defined')
        return self.model.objects.get(pk=id)

    def delete(self, id):
        if not self.model:
            raise TypeError('model not defined')
        self.model.objects.get(id).delete()
