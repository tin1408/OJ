import pymysql
pymysql.install_as_MySQLdb()

from dmoj.celery import app as celery_app
