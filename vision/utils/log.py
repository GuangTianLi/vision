# -*- coding: utf-8 -*-
"""
Copy from Scrapy
"""
import logging
import sys
from logging.config import dictConfig

import vision
from vision.settings import overridden_settings, Settings

logger = logging.getLogger(__name__)


class TopLevelFormatter(logging.Filter):
    """Keep only top level loggers's name (direct children from root) from
    records.

    This filter will replace vision loggers' names with 'vision'. This mimics
    the old vision log behaviour and helps shortening long names.

    Since it can't be set for just one logger (it won't propagate for its
    children), it's going to be set in the root handler, with a parametrized
    `loggers` list where it should act.
    """

    def __init__(self, loggers=None):
        self.loggers = loggers or []

    def filter(self, record):
        if any(record.name.startswith(l + '.') for l in self.loggers):
            record.name = record.name.split('.', 1)[0]
        return True


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'vision': {
            'level': 'DEBUG',
        },
        'twisted': {
            'level': 'ERROR',
        },
    }
}


def configure_logging(settings=None, install_root_handler=True):
    """
    Initialize logging defaults for vision.

    :param settings: settings used to create and configure a handler for the
        root logger (default: None).
    :type settings: dict, :class:`~vision.settings.Settings` object or ``None``

    :param install_root_handler: whether to install root logging handler
        (default: True)
    :type install_root_handler: bool

    This function does:

    - Route warnings and twisted logging through Python standard logging
    - Assign DEBUG and ERROR level to vision and Twisted loggers respectively
    - Route stdout to log if LOG_STDOUT setting is True

    When ``install_root_handler`` is True (default), this function also
    creates a handler for the root logger according to given settings
    (see :ref:`topics-logging-settings`). You can override default options
    using ``settings`` argument. When ``settings`` is empty or None, defaults
    are used.
    """
    if not sys.warnoptions:
        # Route warnings through python logging
        logging.captureWarnings(True)

    dictConfig(DEFAULT_LOGGING)

    if isinstance(settings, dict) or settings is None:
        settings = Settings(settings)

    if settings.getbool('LOG_STDOUT'):
        sys.stdout = StreamLogger(logging.getLogger('stdout'))

    if install_root_handler:
        logging.root.setLevel(logging.NOTSET)
        handler = _get_handler(settings)
        logging.root.addHandler(handler)


def _get_handler(settings):
    """ Return a log handler object according to settings """
    filename = settings.get('LOG_FILE')
    if filename:
        encoding = settings.get('LOG_ENCODING')
        handler = logging.FileHandler(filename, encoding=encoding)
    elif settings.getbool('LOG_ENABLED'):
        handler = logging.StreamHandler()
    else:
        handler = logging.NullHandler()

    formatter = logging.Formatter(
        fmt=settings.get('LOG_FORMAT'),
        datefmt=settings.get('LOG_DATEFORMAT')
    )
    handler.setFormatter(formatter)
    handler.setLevel(settings.get('LOG_LEVEL'))
    handler.addFilter(TopLevelFormatter(['vision']))
    return handler


def log_vision_info(settings):
    logger.info("vision %(version)s started (bot: %(bot)s)",
                {'version': vision.__version__, 'bot': settings['BOT_NAME']})

    d = dict(overridden_settings(settings))
    logger.info("Overridden settings: %(settings)r", {'settings': d})


class StreamLogger(object):
    """Fake file-like stream object that redirects writes to a logger instance

    Taken from:
        http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        for h in self.logger.handlers:
            h.flush()


class LogCounterHandler(logging.Handler):
    """Record log levels count into a crawler stats"""

    def __init__(self, center, *args, **kwargs):
        super(LogCounterHandler, self).__init__(*args, **kwargs)
        self.center = center

    def emit(self, record):
        sname = 'log_count/{}'.format(record.levelname)


def logformatter_adapter(logkws):
    """
    Helper that takes the dictionary output from the methods in LogFormatter
    and adapts it into a tuple of positional arguments for logger.log calls,
    handling backward compatibility as well.
    """

    level = logkws.get('level', logging.INFO)
    message = logkws.get('format', logkws.get('msg'))
    # NOTE: This also handles 'args' being an empty dict, that case doesn't
    # play well in logger.log calls
    args = logkws if not logkws.get('args') else logkws['args']

    return (level, message, args)
