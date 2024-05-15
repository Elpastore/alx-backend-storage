#!/usr/bin/env python3
"""
exercise module
"""
import uuid
import redis
from typing import Union, Callable, Optional


class Cache():
    """
    class Cache
    """
    def __init__(self):
        """
        the __init__ method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        convert the data back to the desired format
        """
        value = self._redis.get(key)
        return fn(value) if fn is not None else value

    def get_string(self, key: str) -> str:
        """
        conversion function to string
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_string(self, key: str) -> str:
        """
        conversion function to int
        """
        return self.get(key, lambda x: int(x))
