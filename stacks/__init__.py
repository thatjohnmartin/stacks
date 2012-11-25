import logging
from django.conf import settings

# logging level is INFO on production, DEBUG if local install
LOG_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
LOG_FORMAT = '%(asctime)s %(process)d %(filename)s(%(lineno)d): %(levelname)s %(message)s'

logging.basicConfig(filename=settings.LOG_FILE, filemode='a', level=LOG_LEVEL, format=LOG_FORMAT)
