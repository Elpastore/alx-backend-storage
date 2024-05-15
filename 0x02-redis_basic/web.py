#!/usr/bin/env python3
"""
web module
"""
import redis
import requests
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_decorator(method: Callable) -> Callable:
    """
    count_decorator decorator that tracks URL access count and caches results.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function for counting and caching.
        """
        key = f'cached:{url}'
        data = r.get(key)
        if data:
            return data.decode("utf-8")

        count = f'count:{url}'
        try:
            page = method(url)
            r.incr(count)
            r.setex(key, 10, page)
            return page
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return f"Error fetching page: {e}"
    return wrapper


@count_decorator
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL using requests.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


if __name__ == '__main__':
    print(get_page('http://slowwly.robertomurray.co.uk'))
