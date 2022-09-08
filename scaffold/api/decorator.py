from functools import wraps
from typing import Callable

from django.http.request import HttpRequest
from django.utils.translation import gettext as _

from .type import TResponses


def has_perm(perm: str):
    def wrapper(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs) -> TResponses:
            requst = (
                args[0]
                if isinstance(args[0], HttpRequest)
                else (kwargs["request"] if isinstance(kwargs.get("request"), HttpRequest) else None)
            )
            if requst:
                if requst.user.has_perm(perm):
                    return func(*args, **kwargs)
                return 403, {"msg": _("You don't have permission")}
            return func(*args, **kwargs)

        return inner

    return wrapper
