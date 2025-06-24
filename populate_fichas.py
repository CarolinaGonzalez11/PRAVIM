import os
import django
import random
from faker import Faker
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pravim.settings')  # Ajusta si tu proyecto tiene otro nombre
django.setup()

from fichas.models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos,
    RedesApoyo, PlanAccion, Egreso, Intervencion,
    Barrio, Cuadrante
)
from fichas.models import (
    DerivacionCavd, DerivacionUravit, DerivacionCdmCai, DerivacionSalud, 
    DerivacionOfam, DerivacionDideco, DerivacionGestionTerritorial,
    DerivacionCapsUdla, DerivacionOln, DerivacionOtro
)
from django.contrib.auth import get_user_model
User = get_user_model()

fake = Faker('es_CL')

# Diagnósticos para AspectosPsicologicos
DIAGNOSTICO_CHOICES = [
    ('estado_animo', 'Trastornos del estado de ánimo'),
    ('ansiedad', 'Trastornos de ansiedad'),
    ('psicoticos', 'Trastornos psicóticos'),
    ('personalidad', 'Trastornos de la personalidad'),
    ('consumo', 'Trastornos por consumo de sustancias'),
    ('neurodesarrollo', 'Trastornos del neurodesarrollo'),
    ('conducta_alimentaria', 'Trastornos de la conducta alimentaria'),
    ('adaptativos', 'Trastornos adaptativos y reacción al estrés'),
    ('somatomorfos', 'Trastornos somatomorfos y psicosomáticos'),
    ('disociativos', 'Trastornos disociativos'),
    ('no_especificado', 'Problemas de salud mental no especificados'),
    ('otro', 'Otro (especifique)')
]

# Obtén o crea un usuario profesional
profesional = User.objects.filter(is_staff=True).first()
if not profesional:
    profesional = User.objects.create_user(username='demo', password='12345', first_name="Demo", last_name="User")

# Asegúrate de que haya barrios y cuadrantes
barrios = list(Barrio.objects.all())
if not barrios:
    for nombre, _ in Barrio.BARRIOS:
        Barrio.objects.create(nombre=nombre)
    barrios = list(Barrio.objects.all())

cuadrantes = list(Cuadrante.objects.all())
if not cuadrantes:
    for nombre, _ in Cuadrante.CUADRANTES:
        Cuadrante.objects.create(nombre=nombre)
    cuadrantes = list(Cuadrante.objects.all())

for i in range(200):
    ficha = FichaAcogida.objects.create(
        estado=random.choice(['ABIERTA', 'CERRADA']),
        profesional=profesional,
        fecha_recepcion=fake.date_between(start_date='-2y', end_date='today'),
        via_ingreso=random.choice([c for c, _ in FichaAcogida.VIA_INGRESO_CHOICES]),
        fecha_contacto_1=fake.date_between(start_date='-2y', end_date='today'),
        tipo_contacto=random.choice([c for c, _ in FichaAcogida.TIPO_CONTACTO_CHOICES]),
        ingreso_efectivo=random.choice([True, False]),
        fecha_ingreso=fake.date_between(start_date='-2y', end_date='today'),
        profesionales_contacto_1=[profesional.get_full_name()],
        contencion_inicial=random.choice([True, False]),
    )
    persona = PersonaAtendida.objects.create(
        ficha=ficha,
        nombre=fake.name(),
        rut_pasaporte=fake.unique.ssn(),
        telefono=fake.phone_number(),
        fecha_nacimiento=fake.date_of_birth(minimum_age=12, maximum_age=75),
        nacionalidad='Chilena',
        estado_civil=random.choice([c for c, _ in PersonaAtendida.ESTADO_CIVIL_CHOICES]),
        prevision=random.choice([c for c, _ in PersonaAtendida.PREVISION_CHOICES]),
        cesfam=random.choice([c for c, _ in PersonaAtendida.CESFAM_CHOICES if c]),  # evita '---------'
        ocupacion=fake.job(),
        villa=fake.street_name(),
        genero=random.choice([c for c, _ in PersonaAtendida.GENERO_CHOICES]),
        discapacidad=random.choice([True, False]),
        etnia=random.choice([True, False]),
        diversidad=random.choice([True, False]),
        direccion=fake.address(),
        barrio=random.choice(barrios),
        cuadrante=random.choice(cuadrantes),
        persona_significativa=fake.name(),
        vinculo=fake.word(ext_word_list=['Amigo', 'Hermana', 'Padre', 'Pareja', 'Vecino']),
        telefono_significativo=fake.phone_number(),
        n_adultos=random.randint(1, 3),
        n_nna=random.randint(0, 3),
    )
    denuncia = Denuncia.objects.create(
        ficha=ficha,
        tiene_denuncia=random.choice([True, False]),
        anio_denuncia=str(fake.year()),
        lugar_denuncia=random.choice([c for c, _ in Denuncia.LUGARES_DENUNCIA]),
        numero_causa=fake.bothify(text="#######"),
        motivo_denuncia=fake.sentence(),
        dificultades=random.choice([c for c, _ in Denuncia.DIFICULTADES_CHOICES]),
        medida_cautelar=random.choice([True, False]),
        medida_cautelar_detalle=fake.sentence(),
    )
    motivo = MotivoIngreso.objects.create(
        ficha=ficha,
        motivo_ingreso=random.choice([c for c, _ in MotivoIngreso.OPCIONES_MOTIVO]),
        descripcion_motivo=fake.text(max_nb_chars=50),
    )
    psicologicos = AspectosPsicologicos.objects.create(
        ficha=ficha,
        antecedentes=fake.sentence(),
        diagnostico=random.choice([c for c, _ in DIAGNOSTICO_CHOICES]),
        afectacion_psicologica=fake.sentence(),
        estado_conciencia=["Lúcido"],
        orientacion=["Desorientación temporal"],
        estado_cognitivo=["Atención"],
    )
    redes = RedesApoyo.objects.create(
        ficha=ficha,
        red_familiares=fake.name(),
        red_amistades=fake.name(),
        red_junta_vecinos=fake.company(),
        red_ong=fake.company(),
    )
    plan = PlanAccion.objects.create(
        ficha=ficha,
        uav_psicologica_1=random.choice([True, False]),
        uav_social_1=random.choice([True, False]),
        patrullaje_activo=random.choice([True, False]),
    )
    egreso = Egreso.objects.create(
        ficha=ficha,
        motivo_egreso=random.choice([c for c, _ in Egreso.MOTIVO_EGRESO_CHOICES]),
        nivel_cumplimiento=random.choice([c for c, _ in Egreso.NIVEL_CUMPLIMIENTO_CHOICES]),
        fecha_egreso=fake.date_between(start_date='-1y', end_date='today')
    )
    # Derivación CAVD
    DerivacionCavd.objects.create(
        ficha=ficha,
        descripcion_cavd=fake.sentence(),
        fecha_derivacion_cavd=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_cavd=random.choice([True, False]),
        fecha_respuesta_cavd=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_cavd=random.choice([True, False]),
        fecha_ingreso_cavd=fake.date_between(start_date='-2y', end_date='today'),
        es_conmocion_publica_cavd=random.choice([True, False]),
        fecha_vinculacion_conmocion_cavd=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación Salud
    DerivacionSalud.objects.create(
        ficha=ficha,
        dispositivo_salud=random.choice([c for c, _ in DerivacionSalud._meta.get_field('dispositivo_salud').choices if c]),
        fecha_derivacion_salud=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_salud=random.choice([True, False]),
        fecha_respuesta_salud=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_salud=random.choice([True, False]),
        fecha_ingreso_salud=fake.date_between(start_date='-2y', end_date='today'),
        dispositivo_salud_otro=fake.company()
    )

    # Derivación Dideco
    DerivacionDideco.objects.create(
        ficha=ficha,
        descripcion_dideco=fake.sentence(),
        fecha_derivacion_dideco=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_dideco=random.choice([True, False]),
        fecha_respuesta_dideco=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_dideco=random.choice([True, False]),
        fecha_ingreso_dideco=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación URAVIT
    DerivacionUravit.objects.create(
        ficha=ficha,
        descripcion_uravit=fake.sentence(),
        fecha_derivacion_uravit=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_uravit=random.choice([True, False]),
        fecha_respuesta_uravit=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación CDM-CAI
    DerivacionCdmCai.objects.create(
        ficha=ficha,
        descripcion_cdm_cai=fake.sentence(),
        fecha_derivacion_cdm_cai=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_cdm_cai=random.choice([True, False]),
        fecha_respuesta_cdm_cai=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_cdm_cai=random.choice([True, False]),
        fecha_ingreso_cdm_cai=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación OFAM
    DerivacionOfam.objects.create(
        ficha=ficha,
        descripcion_ofam=fake.sentence(),
        fecha_derivacion_ofam=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_ofam=random.choice([True, False]),
        fecha_respuesta_ofam=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_ofam=random.choice([True, False]),
        fecha_ingreso_ofam=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación Gestión Territorial
    DerivacionGestionTerritorial.objects.create(
        ficha=ficha,
        descripcion_gestion_territorial=fake.sentence(),
        fecha_derivacion_gestion_territorial=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_gestion_territorial=random.choice([True, False]),
        fecha_respuesta_gestion_territorial=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_gestion_territorial=random.choice([True, False]),
        fecha_ingreso_gestion_territorial=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación CAPS UDLA
    DerivacionCapsUdla.objects.create(
        ficha=ficha,
        descripcion_caps_udla=fake.sentence(),
        fecha_derivacion_caps_udla=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_caps_udla=random.choice([True, False]),
        fecha_respuesta_caps_udla=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_caps_udla=random.choice([True, False]),
        fecha_ingreso_caps_udla=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación OLN
    DerivacionOln.objects.create(
        ficha=ficha,
        descripcion_oln=fake.sentence(),
        fecha_derivacion_oln=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_oln=random.choice([True, False]),
        fecha_respuesta_oln=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_oln=random.choice([True, False]),
        fecha_ingreso_oln=fake.date_between(start_date='-2y', end_date='today')
    )

    # Derivación Otro
    DerivacionOtro.objects.create(
        ficha=ficha,
        institucion_otro=fake.company(),
        descripcion_otro=fake.sentence(),
        fecha_derivacion_otro=fake.date_between(start_date='-2y', end_date='today'),
        es_vinculacion_otro=random.choice([True, False]),
        fecha_respuesta_otro=fake.date_between(start_date='-2y', end_date='today'),
        ingresa_otro=random.choice([True, False]),
        fecha_ingreso_otro=fake.date_between(start_date='-2y', end_date='today')
    )
    # Crea entre 1 y 4 intervenciones para cada ficha
    for j in range(random.randint(1, 4)):
        Intervencion.objects.create(
            ficha=ficha,
            fecha=fake.date_between(start_date=ficha.fecha_recepcion, end_date='today'),
            etapa=random.choice([c for c, _ in Intervencion.ETAPA_CHOICES]),
            tipo_intervencion=random.choice([c for c, _ in Intervencion.TIPO_ATENCION_CHOICES]),
            participantes=fake.name(),
            lugar_via=random.choice([c for c, _ in Intervencion.LUGAR_VIA_CHOICES]),
            objetivos=[fake.sentence() for _ in range(random.randint(1, 2))],  # genera lista de strings
            descripcion=fake.paragraph(),
            resultados=fake.paragraph(),
            profesional=profesional,
            responsables=[profesional.get_full_name()],
        )

    if (i+1) % 20 == 0:
        print(f"Se han creado {i+1} fichas...")

print("Carga masiva completada!")
