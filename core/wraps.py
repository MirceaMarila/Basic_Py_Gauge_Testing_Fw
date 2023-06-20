import time
from functools import wraps

from selenium.common import StaleElementReferenceException, ElementClickInterceptedException


def stale_element_reference(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        ok = False
        for _ in range(20):
            try:
                result = func(*args, **kwargs)
                ok = True
                break
            except StaleElementReferenceException:
                time.sleep(0.5)
                try:
                    args[0].refresh()  # args[0] is self from method
                except:
                    pass

        if ok is False:
            result = func(*args, **kwargs)
        return result

    return wrapper


def element_click_intercepted(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        ok = False
        for _ in range(20):
            try:
                result = func(*args, **kwargs)
                ok = True
                break
            except ElementClickInterceptedException:
                time.sleep(0.5)
                try:
                    args[0].refresh()  # args[0] is self from method
                except:
                    pass

        if ok is False:
            result = func(*args, **kwargs)
        return result

    return wrapper
