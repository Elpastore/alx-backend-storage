#!/usr/bin/env python3
"""
web module
"""
import redis
import requests
from datetime import timedelta
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_decorator(method: Callable) -> Callable:
    """
    count_decorator decorator and returns a Callable
    """
    def wrapper(url: str) -> str:
        """
        wrapper function
        """
        key = f'cached:{url}'
        data = r.get(key)
        if data:
            return data.decode(key)

        count = f'count:{url}'
        page = method(url)

        r.incr(count)
        r.set(key, page)
        r.expire(key, 10)

        return page
    return wrapper


@count_decorator
def get_page(url: str) -> str:
    """
    It uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    request = requests.get(url)
    return request.text


if __name__ == '__main__':
    get_page('http://slowwly.robertomurray.co.uk')
