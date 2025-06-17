from django.contrib import admin
from .models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso,
    AspectosPsicologicos, RedesApoyo, PlanAccion, Egreso,
    Intervencion,
    DerivacionCavd, DerivacionUravit, DerivacionCdmCai,
    DerivacionSalud, DerivacionOfam, DerivacionDideco,
    DerivacionGestionTerritorial, DerivacionCapsUdla,
    DerivacionOln, DerivacionOtro,
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


@admin.register(PlanAccion)
class PlanAccionAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'uav_psicologica_1', 'uav_social_1', 'uav_legal_1',
        'patrullaje_activo'
    ]
    list_filter  = ['patrullaje_activo']
    
@admin.register(DerivacionCavd)
class DerivacionCavdAdmin(admin.ModelAdmin):
    list_display  = [
        'ficha',
        'descripcion_cavd', 'fecha_derivacion_cavd',
        'es_vinculacion_cavd', 'fecha_respuesta_cavd',
        'ingresa_cavd', 'fecha_ingreso_cavd',
        'es_conmocion_publica_cavd', 'fecha_vinculacion_conmocion_cavd'
    ]
    list_filter   = ['es_vinculacion_cavd', 'es_conmocion_publica_cavd']

@admin.register(DerivacionUravit)
class DerivacionUravitAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_uravit', 'fecha_derivacion_uravit',
        'es_vinculacion_uravit', 'fecha_respuesta_uravit'
    ]
    list_filter  = ['es_vinculacion_uravit']

@admin.register(DerivacionCdmCai)
class DerivacionCdmCaiAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_cdm_cai', 'fecha_derivacion_cdm_cai',
        'es_vinculacion_cdm_cai', 'fecha_respuesta_cdm_cai',
        'ingresa_cdm_cai', 'fecha_ingreso_cdm_cai'
    ]
    list_filter  = ['es_vinculacion_cdm_cai']

@admin.register(DerivacionSalud)
class DerivacionSaludAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'dispositivo_salud', 'fecha_derivacion_salud',
        'es_vinculacion_salud', 'fecha_respuesta_salud',
        'ingresa_salud', 'fecha_ingreso_salud'
    ]
    list_filter  = ['dispositivo_salud', 'es_vinculacion_salud']

@admin.register(DerivacionOfam)
class DerivacionOfamAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_ofam', 'fecha_derivacion_ofam',
        'es_vinculacion_ofam', 'fecha_respuesta_ofam',
        'ingresa_ofam', 'fecha_ingreso_ofam'
    ]
    list_filter  = ['es_vinculacion_ofam']

@admin.register(DerivacionDideco)
class DerivacionDidecoAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_dideco', 'fecha_derivacion_dideco',
        'es_vinculacion_dideco', 'fecha_respuesta_dideco',
        'ingresa_dideco', 'fecha_ingreso_dideco'
    ]
    list_filter  = ['es_vinculacion_dideco']

@admin.register(DerivacionGestionTerritorial)
class DerivacionGestionTerritorialAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_gestion_territorial', 'fecha_derivacion_gestion_territorial',
        'es_vinculacion_gestion_territorial', 'fecha_respuesta_gestion_territorial',
        'ingresa_gestion_territorial', 'fecha_ingreso_gestion_territorial'
    ]
    list_filter  = ['es_vinculacion_gestion_territorial']

@admin.register(DerivacionCapsUdla)
class DerivacionCapsUdlaAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_caps_udla', 'fecha_derivacion_caps_udla',
        'es_vinculacion_caps_udla', 'fecha_respuesta_caps_udla',
        'ingresa_caps_udla', 'fecha_ingreso_caps_udla'
    ]
    list_filter  = ['es_vinculacion_caps_udla']

@admin.register(DerivacionOln)
class DerivacionOlnAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'descripcion_oln', 'fecha_derivacion_oln',
        'es_vinculacion_oln', 'fecha_respuesta_oln',
        'ingresa_oln', 'fecha_ingreso_oln'
    ]
    list_filter = ['es_vinculacion_oln']

@admin.register(DerivacionOtro)
class DerivacionOtroAdmin(admin.ModelAdmin):
    list_display = [
        'ficha',
        'institucion_otro', 'descripcion_otro',
        'fecha_derivacion_otro', 'es_vinculacion_otro',
        'fecha_respuesta_otro', 'ingresa_otro',
        'fecha_ingreso_otro'
    ]
    list_filter = ['es_vinculacion_otro']
