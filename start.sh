#!/usr/bin/env bash
# /root/env/project/bin/python /root/env/project/bin/gunicorn auto_test.wsgi --name monitor_new -w 2 -b 0.0.0.0:8000 --daemon

# before use channels
# gunicorn auto_test.wsgi --name auto_test_server --workers 2 --bind 0.0.0.0:8000 --daemon

# http://docs.gunicorn.org/en/latest/settings.html#logging
# https://channels.readthedocs.io/en/latest/deploying.html
# https://www.uvicorn.org/


# new: gunicorn auto_test.asgi:application --name auto_test_server -c gunicorn_config.py --daemon
gunicorn auto_test.asgi:application --name auto_test_server --bind 0.0.0.0:8000 --workers 2 --worker-class uvicorn.workers.UvicornWorker --daemon
