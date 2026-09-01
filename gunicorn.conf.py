# gunicorn.conf.py
import multiprocessing
import os

# Increase timeout to 300 seconds
timeout = 300
graceful_timeout = 300

# Worker settings
workers = 1
worker_class = 'sync'
max_requests = 100
max_requests_jitter = 10

# Bind
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"
