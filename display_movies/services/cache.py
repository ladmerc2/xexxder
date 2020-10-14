import redis
import json

from django.conf import settings


class RedisCache():
    def __init__(self, ttl=60):
        self._redis = redis.StrictRedis(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT, db=0)
        self._ttl = ttl

    def set(self, key: str, value: list):
        """ Set adds a key/value pair to the cache."""
        setValue = self._redis.set(key, json.dumps(value))
        self._redis.expire(key, self._ttl)
        return setValue

    def get(self, key: str):
        """ Get retrieves the value of the given key from cache."""
        value = self._redis.get(key)
        validTypes = type(value) == str or type(value) == bytes
        if value and validTypes:
            value = json.loads(value)
            return value

    def delete(self, key):
        """ Delete key from redis store """
        self._redis.delete(key)
