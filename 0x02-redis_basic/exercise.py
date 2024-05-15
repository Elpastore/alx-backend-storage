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


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    # print(f"{function_name} was called {value} times")
    print("{} was called {} times:".format(function_name, value))
    # inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    # outputs = r.lrange(f"{function_name}:outputs", 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


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
