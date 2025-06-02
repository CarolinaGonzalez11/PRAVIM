from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

class LoginInstitucionalView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        # Aquí puedes controlar a qué vista va cada tipo de usuario
        user = self.request.user
        if user.rol == 'ADMINISTRADOR':
            return '/fichas/ficha-completa/nueva/'  # o una vista inicial de admin
        elif user.rol == 'COORDINACION':
            return '/fichas/ficha-completa/nueva/'  # o el dashboard de coordinación
        elif user.rol == 'PROFESIONAL':
            return '/fichas/ficha-completa/nueva/'  # o un listado de personas
        else:
            return '/login/'  # por si no tiene rol
