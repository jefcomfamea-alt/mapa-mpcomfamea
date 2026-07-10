from functools import wraps
from django.shortcuts import redirect


def grupo_requerido(*grupos_permitidos):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.groups.filter(name__in=grupos_permitidos).exists():
                return view_func(request, *args, **kwargs)

            return redirect("inicio")

        return wrapper

    return decorator