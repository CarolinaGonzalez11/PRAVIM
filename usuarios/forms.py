from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Esto valida el username como si fuera email
        if not user.username.endswith('@maipu.cl'):
            raise ValidationError(
                "Solo se permite acceso con correos institucionales @maipu.cl.",
                code='invalid_login',
            )
