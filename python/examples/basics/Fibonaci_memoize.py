import functools

@functools.lru_cache(maxsize=10)
def fib(num):
    if num < 2:
        return num
    else:
        return fib(num-1) + fib(num-2)
