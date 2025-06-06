from datetime import date
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Barrio(models.Model):
    BARRIOS = [
        ('Ciudad Satélite', 'Ciudad Satélite'),
        ('Clotario Blest', 'Clotario Blest'),
        ('El Abrazo de Maipú', 'El Abrazo de Maipú'),
        ('Esquina Blanca-Cuatro Álamos', 'Esquina Blanca-Cuatro Álamos'),
        ('Hospital-Campos de Batalla', 'Hospital-Campos de Batalla'),
        ('Industrial', 'Industrial'),
        ('La Farfana', 'La Farfana'),
        ('Lo Errazuriz', 'Lo Errazuriz'),
        ('Longitudinal', 'Longitudinal'),
        ('Los Bosquinos', 'Los Bosquinos'),
        ('Los Héroes', 'Los Héroes'),
        ('Maipú Centro', 'Maipú Centro'),
        ('Pajaritos Sur', 'Pajaritos Sur'),
        ('Parque Tres Poniente', 'Parque Tres Poniente'),
        ('Pehuén', 'Pehuén'),
        ('Portal del Sol', 'Portal del Sol'),
        ('Riesco Central', 'Riesco Central'),
        ('Rinconada Rural', 'Rinconada Rural'),
        ('Santa Ana de Chena', 'Santa Ana de Chena'),
        ('Sol Poniente', 'Sol Poniente'),
        ('Templo Votivo', 'Templo Votivo'),
    ]
    nombre = models.CharField(max_length=100, choices=BARRIOS, unique=True)
    def __str__(self):
        return self.nombre


class Cuadrante(models.Model):
    CUADRANTES = [
        ('215-A', '215-A'), ('215-B', '215-B'), ('215-C', '215-C'),
        ('216-A', '216-A'), ('216-B', '216-B'),
        ('217-A', '217-A'), ('217-B', '217-B'),
        ('218-A', '218-A'), ('218-B', '218-B'), ('218-C', '218-C'),
        ('219', '219'), ('220-A', '220-A'), ('220-B', '220-B'),
        ('221-A', '221-A'), ('221-B', '221-B'), ('221-C', '221-C'),
        ('222-A', '222-A'), ('223-A', '223-A'), ('223-B', '223-B'), ('223-C', '223-C'),
        ('SRA', 'SRA'), ('SRB', 'SRB'), ('SRC', 'SRC'),
    ]
    nombre = models.CharField(max_length=20, choices=CUADRANTES, unique=True)
    def __str__(self):
        return self.nombre




class FichaAcogida(models.Model):

    VIA_INGRESO_CHOICES = [
        ('Central 1418', 'Central 1418'),
        ('Alcaldía', 'Alcaldía'),
        ('Depto. Mun', 'Departamento Municipal'),
        ('Org. Ext Mun', 'Organización Externa Municipal'),
        ('Dem Espont', 'Demanda espontánea'),
    ]

    TIPO_CONTACTO_CHOICES = [
        ('Telefónico', 'Telefónico'),
        ('Presencial terreno', 'Presencial en terreno'),
        ('Presencial UAV', 'Presencial en UAV'),
        ('Mail', 'Mail'),
        ('Otro', 'Otro'),
    ]

    ESTADOS = [
        ('EN_CURSO', 'En curso'),
        ('CERRADA', 'Cerrada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='EN_CURSO')
    profesional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_recepcion = models.DateField(null=True, blank=True)
    via_ingreso = models.CharField(max_length=50, choices=VIA_INGRESO_CHOICES)
    fecha_contacto_1 = models.DateField(null=True, blank=True)
    fecha_contacto_2 = models.DateField(null=True, blank=True)
    fecha_contacto_3 = models.DateField(null=True, blank=True)
    tipo_contacto = models.CharField(max_length=50, choices=TIPO_CONTACTO_CHOICES)
    
    ingreso_efectivo = models.BooleanField(default=False)
    fecha_ingreso = models.DateField(null=True, blank=True)
    profesionales_contacto_1 = ArrayField(
        models.CharField(max_length=50), blank=True, null=True
    )
    contencion_inicial = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Ficha {self.id} - {self.fecha_recepcion}"




class PersonaAtendida(models.Model):
    GENERO_CHOICES = [
        ('FEMENINO', 'Femenino'),
        ('MASCULINO', 'Masculino'),
        ('NO_BINARIO', 'No Binario'),
        ('OTRO', 'Otro'),
    ]
    PREVISION_CHOICES = [
        ('FONASA', 'FONASA'),
        ('ISAPRE', 'ISAPRE'),
        ('NINGUNA', 'Ninguna'),
    ]
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero'),
        ('CASADO', 'Casado'),
        ('VIUDO', 'Viudo/a'),
        ('DIVORCIADO', 'Divorciado/a'),
        ('SEPARADO', 'Separado/a'),
        ('ANULADO', 'Anulado'),
        ('CONVIVIENTE', 'Conviviente'),
    ]
    ficha = models.OneToOneField(FichaAcogida, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, blank=True)
    rut_pasaporte = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=50, blank=True)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True)
    prevision = models.CharField(max_length=20, choices=PREVISION_CHOICES, blank=True)
    cesfam = models.CharField(max_length=100, blank=True)
    ocupacion = models.CharField(max_length=100, blank=True)
    villa = models.CharField(max_length=100, blank=True)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    rango_etareo = models.CharField(max_length=10, blank=True)
    discapacidad = models.BooleanField(default=False)
    etnia = models.BooleanField(default=False)
    diversidad = models.BooleanField(default=False)
    direccion = models.CharField(max_length=250, blank=True)
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, null=True, blank=True)
    cuadrante = models.ForeignKey(Cuadrante, on_delete=models.SET_NULL, null=True, blank=True)
    persona_significativa = models.CharField(max_length=100, blank=True)
    vinculo = models.CharField(max_length=100, blank=True)
    telefono_significativo = models.CharField(max_length=20, blank=True)
    n_adultos = models.PositiveIntegerField(default=0)
    n_nna = models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        if self.fecha_nacimiento:
            today = date.today()
            edad = today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
            self.edad = edad
            if edad <= 14:
                self.rango_etareo = "0-14"
            elif edad <= 17:
                self.rango_etareo = "15-17"
            elif edad <= 30:
                self.rango_etareo = "18-30"
            elif edad <= 40:
                self.rango_etareo = "31-40"
            elif edad <= 59:
                self.rango_etareo = "41-59"
            else:
                self.rango_etareo = "60+"
        super().save(*args, **kwargs)


class Denuncia(models.Model):
    LUGARES_DENUNCIA = [
        ('52 COM', '52 COM'),
        ('25 COM', '25 COM'),
        ('SUBCOM', 'SUBCOM'),
        ('PDI', 'PDI'),
        ('FISCALIA', 'FISCALÍA'),
        ('T.DE FAMILIA', 'Tribunal de Familia'),
        ('48 COM FAMILIA', '48 COM FAMILIA'),
        ('OTRO', 'Otro'),
    ]
    DIFICULTADES_CHOICES = [
        ('mal_trato', 'Mal trato/trato inadecuado'),
        ('tiempo_espera', 'Tiempo de espera'),
        ('no_llegaron', 'No llegaron a llamado'),
        ('otra', 'Otra'),
    ]
    ficha = models.OneToOneField(FichaAcogida, on_delete=models.CASCADE)
    tiene_denuncia = models.BooleanField(default=False)
    anio_denuncia = models.CharField(max_length=10, blank=True)
    lugar_denuncia = models.CharField(max_length=50,choices=LUGARES_DENUNCIA, blank=True)
    lugar_denuncia_otro = models.CharField(max_length=100, blank=True)  # campo para especificar "otro"
    numero_causa = models.CharField(max_length=50, blank=True)
    motivo_denuncia = models.TextField(blank=True)

    dificultades = models.CharField(max_length=30, choices=DIFICULTADES_CHOICES, blank=True, null=True)
    dificultades_otra = models.TextField(blank=True)  # descripción si selecciona "Otra"

    medida_cautelar = models.BooleanField(default=False)
    medida_cautelar_detalle = models.CharField(max_length=200, blank=True)  # detalle siempre que sea True

    def __str__(self):
        return f"Denuncia - Ficha {self.ficha.id}"

class MotivoIngreso(models.Model):
    OPCIONES_MOTIVO = [
        ('VIF_MUJER', 'Violencia Intrafamiliar contra la mujer'),
        ('VIF_HOMBRE', 'Violencia Intrafamiliar contra el hombre'),
        ('VIF_NNA', 'Violencia Intrafamiliar contra niño/niña'),
        ('VIF_AM', 'Violencia Intrafamiliar contra adulto mayor'),
        ('VULNERACION_NNA', 'Vulneración de derechos a NNA'),
        # Puedes mantener otros motivos relevantes:
        ('FEMICIDIO', 'Femicidio'),
        ('PARRICIDIO', 'Parricidio'),
        ('SECUESTRO', 'Secuestro / Intento Secuestro'),
        ('DELITO_SEXUAL', 'Delito Sexual'),
        ('ROBO', 'Robo'),
        ('SUSTRACCION', 'Sustracción de Menores'),
        ('HOMICIDIO', 'Homicidio / Cuasidelito de Homicidio'),
        ('BALACERAS', 'Balas Locas / Balaceras'),
        ('LESIONES', 'Lesiones'),
        ('ODIO', 'Crímenes de Odio'),
        ('AMENAZAS', 'Amenazas'),
        ('DAÑOS', 'Daños'),
        ('FALLECIMIENTO', 'Fallecimientos'),
        ('OTROS', 'Otro'),
    ]

    ficha = models.OneToOneField(FichaAcogida, on_delete=models.CASCADE)
    motivo_ingreso = models.CharField(max_length=50, choices=OPCIONES_MOTIVO)
    motivo_otro = models.CharField(max_length=200, blank=True)  # Nuevo campo
    descripcion_motivo = models.TextField(blank=True)


DIAGNOSTICO_CHOICES = [
    ('estado_animo', 'Trastornos del estado de ánimo (depresión, bipolaridad, distimia)'),
    ('ansiedad', 'Trastornos de ansiedad (ansiedad generalizada, crisis de pánico, fobias)'),
    ('psicoticos', 'Trastornos psicóticos (esquizofrenia, delirante, psicosis no especificada)'),
    ('personalidad', 'Trastornos de la personalidad (límite, antisocial, evitativa)'),
    ('consumo', 'Trastornos por consumo de sustancias (alcohol, drogas, psicotrópicos)'),
    ('neurodesarrollo', 'Trastornos del neurodesarrollo (autismo, TDAH, discapacidad intelectual leve)'),
    ('conducta_alimentaria', 'Trastornos de la conducta alimentaria (anorexia, bulimia, atracón)'),
    ('adaptativos', 'Trastornos adaptativos y reacción al estrés (estrés agudo, adaptativo, TEPT)'),
    ('somatomorfos', 'Trastornos somatomorfos y psicosomáticos (somatización, dolor crónico sin causa médica)'),
    ('disociativos', 'Trastornos disociativos (amnesia disociativa, despersonalización)'),
    ('no_especificado', 'Problemas de salud mental no especificados (malestar emocional, síntomas inespecíficos)'),
    ('otro', 'Otro (especifique)')
]

class AspectosPsicologicos(models.Model):
    antecedentes = models.TextField(blank=True)
    diagnostico = models.CharField(max_length=32, choices=DIAGNOSTICO_CHOICES, blank=True)
    diagnostico_otro = models.CharField(max_length=100, blank=True)
    atencion_salud_mental = models.BooleanField(default=False)
    atencion_anio = models.CharField(max_length=4, blank=True)
    atencion_lugar = models.CharField(max_length=100, blank=True)
    internacion = models.BooleanField(default=False)
    internacion_anio = models.CharField(max_length=4, blank=True)
    internacion_lugar = models.CharField(max_length=100, blank=True)
    afectacion_psicologica = models.TextField(blank=True)
    ficha = models.OneToOneField('FichaAcogida', on_delete=models.CASCADE)

    diagnostico_salud_mental = models.TextField(blank=True)
    atenciones_anteriores = models.TextField(blank=True)
    internaciones = models.TextField(blank=True)
    suicidio_antecedentes = models.TextField(blank=True)

    # Campos multiseleccionables (se usarán en el formulario como checkboxes)
    estado_conciencia = models.JSONField(blank=True, null=True)  # ☐ Lúcido ☐ Obnubilado
    orientacion = models.JSONField(blank=True, null=True)        # ☐ Desorientación temporal ☐ Desorientación espacial
    estado_cognitivo = models.JSONField(blank=True, null=True)   # ☐ Atención ☐ Concentración ☐ Memoria

    actitud = models.JSONField(blank=True, null=True)
    lenguaje = models.JSONField(blank=True, null=True)
    afectividad = models.JSONField(blank=True, null=True)
    sueno = models.JSONField(blank=True, null=True)
    alimentacion = models.JSONField(blank=True, null=True)

    limitacion_vida_cotidiana = models.CharField(max_length=100, blank=True)
    quiebre_historia_vida = models.BooleanField(default=False)


class RedesApoyo(models.Model):
    ficha = models.OneToOneField(FichaAcogida, on_delete=models.CASCADE)

    red_familiares = models.TextField(blank=True)
    red_amistades = models.TextField(blank=True)
    red_conyuge = models.TextField(blank=True)
    red_laborales = models.TextField(blank=True)
    red_otros_personales = models.TextField(blank=True)

    red_junta_vecinos = models.TextField(blank=True)
    red_centro_madres = models.TextField(blank=True)
    red_club_adultos = models.TextField(blank=True)
    red_club_deportivo = models.TextField(blank=True)
    red_otros_comunitarios = models.TextField(blank=True)

    red_municipalidad = models.TextField(blank=True)
    red_cesfam = models.TextField(blank=True)
    red_cosam = models.TextField(blank=True)
    red_otro_salud = models.TextField(blank=True)
    red_establecimiento = models.TextField(blank=True)
    red_ong = models.TextField(blank=True)



class Egreso(models.Model):
    MOTIVO_EGRESO_CHOICES = [
        ('Derivación y vinculación a red de Atención', 'Derivación y vinculación a red de Atención'),
        ('Cierre de proceso de intervención', 'Cierre de proceso de intervención'),
        ('Desiste de apoyo de la UAV', 'Desiste de apoyo de la UAV'),
        ('Cierre administrativo', 'Cierre administrativo'),
        ('No requiere apoyo posterior', 'No requiere apoyo posterior'),
        ('Otra', 'Otra'),
    ]

    NIVEL_CUMPLIMIENTO_CHOICES = [
        ('Cumplimiento satisfactorio', 'Cumplimiento satisfactorio'),
        ('Cumplimiento parcial', 'Cumplimiento parcial'),
        ('No cumplimiento', 'No cumplimiento'),
        ('NC', 'NC'),
    ]

    ficha = models.OneToOneField(FichaAcogida, on_delete=models.CASCADE)
    motivo_egreso = models.CharField(max_length=100, choices=MOTIVO_EGRESO_CHOICES, blank=True)
    nivel_cumplimiento = models.CharField(max_length=50, choices=NIVEL_CUMPLIMIENTO_CHOICES, blank=True)
    fecha_egreso = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Egreso - Ficha {self.ficha.id}"


class Intervencion(models.Model):
    ETAPA_CHOICES = [
        ('Diagnóstico', 'Diagnóstico'),
        ('Intervención', 'Intervención'),
        ('Preparación Egreso/Egreso', 'Preparación Egreso/Egreso'),
    ]

    TIPO_ATENCION_CHOICES = [
        ('Psicológica', 'Psicológica'),
        ('Social', 'Social'),
        ('Psicosocial', 'Psicosocial'),
        ('Vinculación con red', 'Vinculación con red'),
        ('Otra', 'Otra'),
    ]

    LUGAR_VIA_CHOICES = [
        ('Domicilio', 'Domicilio'),
        ('Otro sitio en terreno', 'Otro sitio en terreno'),
        ('Contacto telefónico', 'Contacto telefónico'),
        ('Video llamada', 'Video llamada'),
        ('Dependencias UAV', 'Dependencias UAV'),
        ('Correo, e-mail', 'Correo, e-mail'),
        ('Otro', 'Otro'),
    ]

    ficha = models.ForeignKey(FichaAcogida, on_delete=models.CASCADE)
    fecha = models.DateField()
    etapa = models.CharField(max_length=50, choices=ETAPA_CHOICES)
    tipo_intervencion = models.CharField(max_length=50, choices=TIPO_ATENCION_CHOICES)
    responsables = models.CharField(max_length=200, blank=True)
    participantes = models.CharField(max_length=200, blank=True)
    lugar_via = models.CharField(max_length=50, choices=LUGAR_VIA_CHOICES)
    objetivos = models.TextField(blank=True)
    descripcion = models.TextField(blank=True)
    resultados = models.TextField(blank=True)
    profesional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"Intervención {self.fecha} - Ficha {self.ficha.id}"

class PlanAccion(models.Model):
    ficha = models.OneToOneField(FichaAcogida, on_delete=models.CASCADE)

    # Derivación CAVD
    derivacion_cavd_psicologica = models.BooleanField(default=False)
    derivacion_cavd_juridica = models.BooleanField(default=False)

    # Derivación CESFAM
    derivacion_cesfam_salud_general = models.BooleanField(default=False)
    derivacion_cesfam_salud_mental = models.BooleanField(default=False)

    # UAV Atención Psicológica (checkbox + texto)
    uav_psicologica_1 = models.BooleanField(default=False)
    uav_psicologica_1_detalle = models.TextField(blank=True)

    uav_psicologica_2 = models.BooleanField(default=False)
    uav_psicologica_2_detalle = models.TextField(blank=True)

    uav_psicologica_3 = models.BooleanField(default=False)
    uav_psicologica_3_detalle = models.TextField(blank=True)

    # UAV Atención Social (checkbox + texto)
    uav_social_1 = models.BooleanField(default=False)
    uav_social_1_detalle = models.TextField(blank=True)

    uav_social_2 = models.BooleanField(default=False)
    uav_social_2_detalle = models.TextField(blank=True)

    uav_social_3 = models.BooleanField(default=False)
    uav_social_3_detalle = models.TextField(blank=True)

    # UAV Atención Legal (checkbox + texto)

    uav_legal_1 = models.BooleanField(default=False)
    uav_legal_1_detalle = models.TextField(blank=True)

    uav_legal_2 = models.BooleanField(default=False)
    uav_legal_2_detalle = models.TextField(blank=True)

    uav_legal_3 = models.BooleanField(default=False)
    uav_legal_3_detalle = models.TextField(blank=True)
    
    # Patrullaje Preventivo
    patrullaje_activo = models.BooleanField(default=False)

    patrullaje_turno_1 = models.BooleanField(default=False)
    patrullaje_entrevista_1 = models.BooleanField(default=False)

    patrullaje_turno_2 = models.BooleanField(default=False)
    patrullaje_entrevista_2 = models.BooleanField(default=False)

    patrullaje_turno_3 = models.BooleanField(default=False)
    patrullaje_entrevista_3 = models.BooleanField(default=False)

    registro_patrullaje = models.CharField(max_length=20, blank=True)  # ej: 2025-0001

    # Profesional a cargo
    profesional_nathaly = models.BooleanField(default=False)
    profesional_paloma = models.BooleanField(default=False)
    cordinadora_gloria = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Plan de Acción - Ficha {self.ficha.id}"
