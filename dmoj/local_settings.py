import os

IN_DOCKER = os.environ.get('IN_DOCKER', False)

DB_HOST = 'vnoi-db' if IN_DOCKER else '127.0.0.1'
REDIS_HOST = 'vnoi-redis' if IN_DOCKER else '127.0.0.1'
DATA_DIR = '/app/data' if IN_DOCKER else '/Users/tinduong/Documents/interich/cham_online/vnoi_data'

SECRET_KEY = os.environ.get('SECRET_KEY', 'change_me_to_a_random_secret_key')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmoj',
        'USER': 'dmoj',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'vnoj_pass_123'),
        'HOST': DB_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': 'SET foreign_key_checks = 0',
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379/0'

CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379/0'

DMOJ_PROBLEM_DATA_ROOT = os.path.join(DATA_DIR, 'problems')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'collected_static')
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources'),
    os.path.join(DATA_DIR, 'static'),
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SEND_ACTIVATION_EMAIL = False
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7

# Bridged configuration
if IN_DOCKER:
    BRIDGED_DJANGO_ADDRESS = [('0.0.0.0' if os.environ.get('IS_BRIDGED') else 'vnoi-bridged', 9998)]
    BRIDGED_JUDGE_ADDRESS = [('0.0.0.0', 9999)]
else:
    BRIDGED_DJANGO_ADDRESS = [('127.0.0.1', 9998)]
    BRIDGED_JUDGE_ADDRESS = [('127.0.0.1', 9999)]


# Event Server Configuration
EVENT_DAEMON_USE = True
EVENT_DAEMON_POST = 'ws://vnoi-wsevent:15101/' if IN_DOCKER else 'ws://127.0.0.1:15101/'
EVENT_DAEMON_GET = 'ws://localhost:15100/'
EVENT_DAEMON_POLL = 'http://localhost:15102/channels/'
EVENT_DAEMON_SUBMISSION_KEY = os.environ.get('JUDGE_KEY', 'change_me_judge_key')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'judge.bridge': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

