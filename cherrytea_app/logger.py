import logging
import json

from django.core import serializers


class Logger(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def _log(self, level, message, models):
        msg = {
            'message': message,
            'data': json.loads(serializers.serialize('json', models))  # this is retarded sam, jesus christ todo
        }
        self._logger.log(level, json.dumps(msg))

    def info(self, message, *models):
        self._log('INFO', message, *models)

    def error(self, message, *models):
        self._log('ERROR', message, *models)

    def warning(self, message, *models):
        self._log('WARNING', message, *models)

    def debug(self, message, *models):
        self._log('DEBUG', message, *models)
