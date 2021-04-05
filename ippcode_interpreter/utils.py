from .exception import IPPRuntimeError
import functools
import traceback
import typing
import sys 

@functools.lru_cache()
def wrap_with_logging(callable: typing.Callable = None) -> typing.Callable:
    """
    Wraps a Event Listener Task and adds logging and simple caching to it

    :param callable: Function that should be wrapped
    """
    def decorator(callable: typing.Callable) -> typing.Callable:
        @functools.wraps(callable)
        def wrapper(*args, **kwargs):
            try:
                return callable(*args, **kwargs)
            except Exception as e:
                raise IPPRuntimeError(f"{sys.exc_info()[0].__name__}: {e}") from e

        return wrapper  # func can still be used normally outside

    if callable is None:
        return decorator
    else:
        return decorator(callable)
