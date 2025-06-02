from django.core.exceptions import PermissionDenied
from functools import wraps

def rol_requerido(rol_objetivo):
    """
    Permite el acceso solo a usuarios con el rol exacto especificado.
    """
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.rol != rol_objetivo:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorador

def rol_en_permitidos(roles_permitidos):
    """
    Permite el acceso solo si el usuario tiene un rol dentro de los roles permitidos.
    """
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.rol not in roles_permitidos:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorador
