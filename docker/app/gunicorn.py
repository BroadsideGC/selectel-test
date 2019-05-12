import os
import multiprocessing


bind = '0.0.0.0:{}'.format(os.getenv('PORT'))
workers = multiprocessing.cpu_count() * 2 + 1
chdir = '/opt/'
user = 'root'
max_requests = 5000
max_requests_jitter = 100
