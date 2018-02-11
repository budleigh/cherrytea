import logging
import json

from django.core import serializers


class Logger(object):
    """
    Wraps normal logger with serialization for django models.
    """

    def __init__(self):
        self._logger = logging.getLogger('cherrytea')

    def _log(self, level, message, *models):
        msg = {
            'message': message,
            'data': json.loads(serializers.serialize('json', models))  # this is retarded sam, jesus christ todo
        }
        self._logger.log(level, json.dumps(msg))

    def info(self, message, *models):
        self._log(logging.INFO, message, *models)

    def error(self, message, *models):
        self._log(logging.ERROR, message, *models)

    def warning(self, message, *models):
        self._log(logging.WARN, message, *models)

    def debug(self, message, *models):
        self._log(logging.DEBUG, message, *models)
