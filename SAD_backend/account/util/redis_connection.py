import redis
from django.conf import settings

connection = redis.StrictRedis(host=settings.REDIS_HOST,
                               port=settings.REDIS_PORT, db=0)
