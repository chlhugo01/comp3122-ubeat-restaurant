import json
import redis
import requests
import random
from datetime import datetime


redis_conn = redis.Redis(host='message_queue', port=6379)
r_id = random.randint(1111,9999)
r_id_str = str(r_id)
