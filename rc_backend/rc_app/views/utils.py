from functools import wraps

from django.http import HttpResponseNotAllowed


def force_post(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseNotAllowed("method not allowed")
        return function(request, *args, **kwargs)

    return wrapper


def force_get(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.method != "GET":
            return HttpResponseNotAllowed("method not allowed")
        return function(request, *args, **kwargs)

    return wrapper
