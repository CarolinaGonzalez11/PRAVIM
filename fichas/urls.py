from django.urls import path
from . import views

app_name = 'fichas'

urlpatterns = [
    path('ficha-completa/nueva/', views.crear_ficha_completa, name='ficha_completa_nueva'),
    path('ficha-completa/<int:ficha_id>/', views.ver_ficha_completa, name='ver_ficha_completa'),
    path('ficha-completa/<int:ficha_id>/editar/', views.editar_ficha_completa, name='editar_ficha_completa'),  # <--- nueva ruta
    path('buscar-persona/', views.buscar_persona, name='buscar_persona'),
    path('ingresar-intervencion/', views.ingresar_intervencion, name='ingresar_intervencion'),
    path('api/intervencion/guardar/<int:ficha_id>/', views.api_intervencion_guardar, name='api_intervencion_guardar'),
    path('api/intervencion/editar/<int:intervencion_id>/', views.api_intervencion_editar, name='api_intervencion_editar'),
    path('gestionar-egreso/<int:ficha_id>/', views.gestionar_egreso, name='gestionar_egreso'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
