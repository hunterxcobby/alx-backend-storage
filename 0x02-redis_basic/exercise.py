#!/usr/bin/env python3

""" Module that contains the Cache class.
This module demonstrates how to use Redis as a cache.
"""

import redis  # Import the Redis library for interacting with Redis
# Import the uuid module for generating random keys
import uuid
# Import Union from typing module for type annotations
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: Decorated method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # get function name from the wrapped function
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function in Redis.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: Decorated method.
    """
    key = method.__qualname__
    # Generate keys for inputs and outputs lists
    inputs_key = f"{key}:inputs"
    outputs_key = f"{key}:outputs"

    def wrapper(self, *args, **kwargs):
        # Execute the original method and retrieve the output
        output = method(self, *args, **kwargs)

        # Store the input in the inputs list
        self._redis.lpush(inputs_key, output)
        # Store the output in the outputs list
        self._redis.rpush(outputs_key, str(args))

        # Return the output
        return output

    return wrapper


class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        This method creates an instance of the Redis client
        and flushes the Redis database.
        """
        self._redis = redis.Redis(
            host='localhost', port=6379, db=0)  # Initialize Redis client
        self._redis.flushdb()  # Flush the Redis database

    # Decorate the store method with the count_calls decorator
    @count_calls
    # Decorate the store method with the call_history decorator
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in Redis.
        Returns:
            str: The randomly generated key under which
            the data is stored in Redis.
        """
        key = str(uuid.uuid4())  # Generate a random key using uuid
        # Store the data in Redis with the generated key
        self._redis.set(key, data)
        return key  # Return the generated key

    def get(self, key: str,
            fn: Callable = None) -> Union[str,
                                          bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key.
        Args:
            key (str): The key under which the data is stored in Redis.
            fn (Callable, optional):
            A callable function to convert the data to desired format.
        Returns:
            Union[str, bytes, int, float, None]: The data retrieved from Redis,
            optionally converted by fn.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data) if data else None
        else:
            return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve string data from Redis using the provided key.
        Args:
            key (str): The key under which the string data is stored in Redis.
        Returns:
            Union[str, None]: The string data retrieved from
            Redis, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve integer data from Redis using the provided key.
        Args:
            key (str): The key under which the integer data is stored in Redis.
        Returns:
            Union[int, None]: The integer data retrieved from
            Redis, or None if the key does not exist.
        """
        return self.get(key, fn=int)

    def replay(self, method):
        """
        Display the history of calls of a particular function.
        Args:
            method (Callable): The method to display the history for.
        """
        key = method.__qualname__
        key_inputs = key + ":inputs"
        key_outputs = key + ":outputs"
        # The count_calls decorator, when applied to
        # the store method, uses a separate key
        # derived from the method's qualified name
        # ("Cache.store" in this case) to keep
        # track of how many times the store method has been called.
        # This is a different key from the UUIDs used for storing data.
        count = self.get(key).decode("utf-8")
        print(f"Cache.{key} was called {count} times:")
        inputs = self._redis.lrange(key_inputs, 0, -1)
        outputs = self._redis.lrange(key_outputs, 0, -1)
        zipped_list = list(zip(inputs, outputs))

        for i, (input, output) in enumerate(zipped_list):
            print(f"{key} (*{output}) -> {input}")
