#!/usr/bin/env python3
"""
exercise module
"""
import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count_calls decorator and returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """function decorator"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    call_history decorator and return a Callable
    """
    inputs_key = method.__qualname__ + ":inputs"
    outputs_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        function decorator
        """
        self._redis.rpush(inputs_key, str(args))
        outputs = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(outputs))
        return outputs

    return wrapper


def replay(method: Callable):
    """
    display the history of a function
    """
    method_name = method.__qualname__
    inputs_key = method_name + ":inputs"
    outputs_key = method_name + ":outputs"
    cache = redis.Redis()

    # Retrieve history from redis
    input_history = cache.lrange(inputs_key, 0, -1)
    output_history = cache.lrange(outputs_key, 0, -1)

    # Display the history
    # print(f"{method_name} was called {len(input_history)} times:")
    print(f"{method_name} was called {int(cache.get(method_name))} times:")
    for input_args, output in zip(input_history, output_history):
        input_args_str = input_args.decode("utf-8") \
            if isinstance(input_args, bytes) else input_args
        output_str = output.decode("utf-8") \
            if isinstance(output, bytes) else output
        print(f"{method_name}(*{input_args_str}) -> {output_str}")


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

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes, int, float, None]:
        """
        convert the data back to the desired format
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn is not None else value

    def get_str(self, key: str) -> Union[str, None]:
        """
        conversion function to str
        """
        return self.get(key, lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    def get_int(self, key: str) -> Union[int, None]:
        """
        conversion function to if
        """
        return self.get(key, lambda x: int(x) if isinstance(x, bytes) else x)
