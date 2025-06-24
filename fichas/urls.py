from django.urls import path
from . import views
from .views import descargar_derivacion_excel , buscar_persona_excel


app_name = 'fichas'

urlpatterns = [
    path('ficha-completa/nueva/', views.crear_ficha_completa, name='ficha_completa_nueva'),
    path('ficha-completa/<int:ficha_id>/', views.ver_ficha_completa, name='ver_ficha_completa'),
    path('ficha-completa/<int:ficha_id>/editar/', views.editar_ficha, name='editar_ficha_completa'),
    path('buscar-persona/', views.buscar_persona, name='buscar_persona'),
    path('ingresar-intervencion/', views.ingresar_intervencion, name='ingresar_intervencion'),
    path('api/intervencion/guardar/<int:ficha_id>/', views.api_intervencion_guardar, name='api_intervencion_guardar'),
    path('api/intervencion/editar/<int:intervencion_id>/', views.api_intervencion_editar, name='api_intervencion_editar'),
    path('gestionar-egreso/<int:ficha_id>/', views.gestionar_egreso, name='gestionar_egreso'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/intervencion/eliminar/<int:intervencion_id>/', views.api_intervencion_eliminar, name='api_intervencion_eliminar'),
    path('buscar_derivacion/', views.buscar_derivacion, name='buscar_derivacion'),
    path('ficha/<int:ficha_id>/pdf/', views.ficha_pdf, name='ficha_pdf'),
    path('ficha/<int:ficha_id>/preview/', views.ficha_pdf_preview, name='ficha_pdf_preview'),
    path('dashboard/export-excel/', views.dashboard_export_excel, name='dashboard_export_excel'),
    path('historial/', views.historial_cambios, name='historial_cambios'),
    path('ficha/<int:ficha_id>/historial/', views.historial_ficha, name='historial_ficha'),
    path('historial/descargar_excel/', views.descargar_historial_excel, name='descargar_historial_excel'),
    path('derivaciones/descargar_excel/', descargar_derivacion_excel, name='descargar_derivacion_excel'),
    path('buscar-persona/excel/', buscar_persona_excel, name='buscar_persona_excel'),

]
