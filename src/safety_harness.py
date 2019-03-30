import math


def safety_harness(function):

    def safe_function(*args, **kwargs):
        result = 0
        try:
            result = function(*args, **kwargs)
            if math.isnan(result):
                result = 0
        except (ZeroDivisionError, ValueError):
            pass
        return result

    return safe_function