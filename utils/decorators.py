import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def _w(*a, **k):
        t0 = time.time()
        out = func(*a, **k)
        _w.last_runtime_s = time.time() - t0
        return out
    _w.last_runtime_s = None
    return _w

def log_call(logger_name="APP"):
    def deco(func):
        @wraps(func)
        def _w(*a, **k):
            print(f"[{logger_name}] {func.__name__} called")
            return func(*a, **k)
        return _w
    return deco

def ensure_input(expected_types: tuple):
    def deco(func):
        @wraps(func)
        def _w(self, input_data, *a, **k):
            if not isinstance(input_data, expected_types):
                raise TypeError(f"Expected {expected_types}, got {type(input_data)}")
            return func(self, input_data, *a, **k)
        return _w
    return deco
