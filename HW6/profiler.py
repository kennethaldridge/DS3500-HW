"""
File: profiler.py
Description: Using decorators to build out a
well-functioned profiling tool
"""
from collections import defaultdict
import time


def profile(f):
    return Profiler.profile(f)


class Profiler:

    calls = defaultdict(int)  # func name --> # calls
    time = defaultdict(float) # func name --> # total time

    @staticmethod
    def _add(function_name, sec):
        Profiler.calls[function_name] += 1
        Profiler.time[function_name] += sec

    @staticmethod
    def profile(f):
        def wrapper(*args, **kwargs):
            function_name = f.__name__
            start = time.time_ns()
            val = f(*args, **kwargs)
            sec = (time.time_ns() - start) / 10**9
            Profiler._add(function_name, sec)
            return val  # OOPS! We forgot this before! Very important!
        return wrapper

    @staticmethod
    def report():
        """ Summarize # calls, total runtime, and time/call for each function """
        print("Function              Calls     TotSec   Sec/Call")
        for name, num in Profiler.calls.items():
            sec = Profiler.time[name]
            print(f'{name:20s} {num:6d} {sec:10.6f} {sec / num:10.6f}')
