from .common import *


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),   
            'formatter': 'simple',     
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s'
        },
    },

}

