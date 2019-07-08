#from logging import Formatter, FileHandler
from logging.config import dictConfig
import logging

def config_logger(app):
    dictConfig = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
            }
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': "test.log",
                'maxBytes': 5000000,
                'backupCount': 10
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
            },
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'loggers': {
            'flaskApp': {
                'handlers': ["default","wsgi","console"],
                'level': 'DEBUG',
            },
        },
        'root': {
            'handlers': ["console"],
            'level': 'DEBUG',
        },
    }
    logger = logging.getLogger('flaskApp')

    for handler in logger.handlers:
        app.logger.addHandler(handler)
    app.logger.info("Logger configurated")