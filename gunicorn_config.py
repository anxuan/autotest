# coding=utf-8
"""
start cmd: /path/to/gunicorn app_module:app -c /path/to/gunicorn_config.py
e.g.: gunicorn auto_test.asgi:application --name auto_test_server -c gunicorn_config.py --daemon

"""
import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

print('path_of_current_file:%s' % path_of_current_file)
print('path_of_current_dir:%s' % path_of_current_dir)

if not os.path.exists(path_of_current_dir):
    os.mkdir(path_of_current_dir)
if not os.path.exists('logs'):
    os.mkdir('logs')
if not os.path.exists('run'):
    os.mkdir('run')

_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)

worker_class = 'uvicorn.workers.UvicornWorker'  # 'sync'
workers = 2  # multiprocessing.cpu_count() * 2 + 1

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'info'

reload = True
debug = True  # False

bind = "%s:%s" % ("0.0.0.0", 8000)
pidfile = '%s/run/%s.pid' % (path_of_current_dir, _file_name)
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)


