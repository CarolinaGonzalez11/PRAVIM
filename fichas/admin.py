from django.contrib import admin
from .models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso,
    AspectosPsicologicos, RedesApoyo, Egreso, Intervencion,
    Barrio, Cuadrante
)


@admin.register(FichaAcogida)
class FichaAcogidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_recepcion', 'via_ingreso', 'profesional']
    list_filter = ['via_ingreso', 'fecha_recepcion']
    search_fields = ['id', 'profesional__email']
    ordering = ['-fecha_recepcion']


@admin.register(PersonaAtendida)
class PersonaAtendidaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut_pasaporte', 'barrio', 'cuadrante']
    search_fields = ['nombre', 'rut_pasaporte']
    list_filter = ['barrio', 'cuadrante', 'genero']


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ['ficha', 'tiene_denuncia', 'lugar_denuncia', 'numero_causa']
    list_filter = ['tiene_denuncia', 'lugar_denuncia']


@admin.register(MotivoIngreso)
class MotivoIngresoAdmin(admin.ModelAdmin):
    list_display = ['ficha', 'motivo_ingreso']


@admin.register(AspectosPsicologicos)
class AspectosPsicologicosAdmin(admin.ModelAdmin):
    list_display = ['ficha', 'estado_conciencia', 'orientacion', 'quiebre_historia_vida']


@admin.register(RedesApoyo)
class RedesApoyoAdmin(admin.ModelAdmin):
    list_display = ['ficha', 'red_familiares', 'red_amistades', 'red_ong']


@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = ['ficha', 'motivo_egreso', 'nivel_cumplimiento', 'fecha_egreso']
    list_filter = ['motivo_egreso', 'nivel_cumplimiento']


@admin.register(Intervencion)
class IntervencionAdmin(admin.ModelAdmin):
    list_display = ['ficha', 'fecha', 'tipo_intervencion', 'profesional']
    list_filter = ['fecha', 'tipo_intervencion']
    search_fields = ['detalle', 'profesional__email']


@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ['nombre']


@admin.register(Cuadrante)
class CuadranteAdmin(admin.ModelAdmin):
    list_display = ['nombre']
