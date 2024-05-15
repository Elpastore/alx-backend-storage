#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''

import requests
import redis
import time

def get_page(url: str) -> str:
    # Initialize Redis connection
    r = redis.Redis()

    # Increment access count for the URL
    url_count_key = f"count:{url}"
    r.incr(url_count_key)

    # Check if the cached content exists
    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text

        # Cache the HTML content with a timeout of 10 seconds
        r.setex(url, 10, html_content)

        return html_content
    else:
        return f"Failed to fetch page: {url}"
