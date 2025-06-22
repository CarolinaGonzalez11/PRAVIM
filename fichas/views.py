from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos, RedesApoyo, PlanAccion, Egreso
from .forms import (
    FichaAcogidaForm,
    PersonaAtendidaForm,
    DenunciaForm,
    MotivoIngresoForm,
    AspectosPsicologicosForm,
    RedesApoyoForm,
    PlanAccionForm,
    IntervencionForm,
    EgresoForm
    )
from django.forms import modelformset_factory
from datetime import datetime
from datetime import date, timedelta


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos,
    RedesApoyo, PlanAccion
)
from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm,
    MotivoIngresoForm, AspectosPsicologicosForm, RedesApoyoForm,
    PlanAccionForm, EgresoForm,
    DerivacionCavdForm, DerivacionUravitForm, DerivacionCdmCaiForm,
    DerivacionSaludForm, DerivacionOfamForm, DerivacionDidecoForm,
    DerivacionGestionTerritorialForm, DerivacionCapsUdlaForm,
    DerivacionOlnForm, DerivacionOtroForm
)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import FichaAcogida
from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm, MotivoIngresoForm,
    AspectosPsicologicosForm, RedesApoyoForm, PlanAccionForm, EgresoForm,
    DerivacionCavdForm, DerivacionUravitForm, DerivacionCdmCaiForm,
    DerivacionSaludForm, DerivacionOfamForm, DerivacionDidecoForm,
    DerivacionGestionTerritorialForm, DerivacionCapsUdlaForm,
    DerivacionOlnForm, DerivacionOtroForm
)

DERIV_FORMS = [
    ('cavd', DerivacionCavdForm),
    ('uravit', DerivacionUravitForm),
    ('cdm_cai', DerivacionCdmCaiForm),
    ('salud', DerivacionSaludForm),
    ('ofam', DerivacionOfamForm),
    ('dideco', DerivacionDidecoForm),
    ('gestion_territorial', DerivacionGestionTerritorialForm),
    ('caps_udla', DerivacionCapsUdlaForm),
    ('oln', DerivacionOlnForm),
    ('otro', DerivacionOtroForm),
]

@login_required
def crear_ficha_completa(request):
    # Formularios principales
    if request.method == 'POST':
        form_ficha    = FichaAcogidaForm(request.POST, prefix='ficha')
        form_persona  = PersonaAtendidaForm(request.POST, prefix='persona')
        form_denuncia = DenunciaForm(request.POST, prefix='denuncia')
        form_motivo   = MotivoIngresoForm(request.POST, prefix='motivo')
        form_psico    = AspectosPsicologicosForm(request.POST, prefix='psico')
        form_redes    = RedesApoyoForm(request.POST, prefix='redes')
        form_plan     = PlanAccionForm(request.POST, prefix='plan')
        form_egreso   = EgresoForm(request.POST, prefix='egreso')

        # Formularios de derivación
        deriv_forms = {
            key: form_cls(request.POST, prefix=f'deriv_{key}')
            for key, form_cls in DERIV_FORMS
        }

        # Validación conjunta de los principales
        principales_valid = all([
            form_ficha.is_valid(), form_persona.is_valid(), form_denuncia.is_valid(),
            form_motivo.is_valid(), form_psico.is_valid(),
            form_redes.is_valid(), form_plan.is_valid(), form_egreso.is_valid()
        ])

        if principales_valid:
            # Guardar ficha y relacionados
            ficha = form_ficha.save(commit=False)
            ficha.profesional = request.user
            ficha.save()

            for form, rel_name in [
                (form_persona, 'personaatendida'),
                (form_denuncia, 'denuncia'),
                (form_motivo, 'motivoingreso'),
                (form_psico, 'aspectospsicologicos'),
                (form_redes, 'redesapoyo'),
                (form_plan, 'planaccion'),
                (form_egreso, 'egreso'),
            ]:
                obj = form.save(commit=False)
                obj.ficha = ficha
                obj.save()

            # Guardar solo las derivaciones con el checkbox marcado
            for key, deriv_form in deriv_forms.items():
                # asumimos que en tu template pones <input type="checkbox" name="deriv_<key>-check" ...>
                if request.POST.get(f'deriv_{key}-check'):
                    if deriv_form.is_valid():
                        drv = deriv_form.save(commit=False)
                        drv.ficha = ficha
                        drv.save()
            return redirect(f'{reverse("fichas:ver_ficha_completa", args=[ficha.id])}?guardado=1')
    else:
        # GET: instanciar vacíos
        form_ficha    = FichaAcogidaForm(prefix='ficha')
        form_persona  = PersonaAtendidaForm(prefix='persona')
        form_denuncia = DenunciaForm(prefix='denuncia')
        form_motivo   = MotivoIngresoForm(prefix='motivo')
        form_psico    = AspectosPsicologicosForm(prefix='psico')
        form_redes    = RedesApoyoForm(prefix='redes')
        form_plan     = PlanAccionForm(prefix='plan')
        form_egreso   = EgresoForm(prefix='egreso')
        deriv_forms   = {
            key: form_cls(prefix=f'deriv_{key}')
            for key, form_cls in DERIV_FORMS
        }

    context = {
        **{f'form_{n}': f for n, f in [
            ('ficha', form_ficha), ('persona', form_persona),
            ('denuncia', form_denuncia), ('motivo', form_motivo),
            ('psico', form_psico), ('redes', form_redes),
            ('plan', form_plan), ('egreso', form_egreso),
        ]},
        **{f'deriv_{k}': f for k, f in deriv_forms.items()},
        'forms_list': [form_ficha, form_persona, form_denuncia,
                       form_motivo, form_psico, form_redes,
                       form_plan, form_egreso] + list(deriv_forms.values()),
    }
    return render(request, 'fichas/ficha_completa.html', context)

# fichas/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso,
    AspectosPsicologicos, RedesApoyo, PlanAccion
)
from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm, MotivoIngresoForm,
    AspectosPsicologicosForm, RedesApoyoForm, PlanAccionForm
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import (
    FichaAcogida,
    PersonaAtendida,
    Denuncia,
    MotivoIngreso,
    AspectosPsicologicos,
    RedesApoyo,
    PlanAccion,
    Egreso,
    Intervencion,
    # Derivaciones:
    DerivacionCavd,  # <--- Este es el nombre correcto, NO "DerivacionCAVD"
    DerivacionUravit,
    DerivacionCdmCai,
    DerivacionSalud,
    DerivacionOfam,
    DerivacionDideco,
    DerivacionGestionTerritorial,
    DerivacionCapsUdla,
    DerivacionOln,
    DerivacionOtro,
)
from django.forms import modelform_factory
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos,
    RedesApoyo, PlanAccion,
    DerivacionCavd, DerivacionUravit, DerivacionCdmCai, DerivacionSalud,
    DerivacionOfam, DerivacionDideco, DerivacionGestionTerritorial,
    DerivacionCapsUdla, DerivacionOln, DerivacionOtro,
)

from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm, MotivoIngresoForm,
    AspectosPsicologicosForm, RedesApoyoForm, PlanAccionForm,
    DerivacionCavdForm, DerivacionUravitForm, DerivacionCdmCaiForm, DerivacionSaludForm,
    DerivacionOfamForm, DerivacionDidecoForm, DerivacionGestionTerritorialForm,
    DerivacionCapsUdlaForm, DerivacionOlnForm, DerivacionOtroForm,
)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos,
    RedesApoyo, PlanAccion,
    DerivacionCavd, DerivacionUravit, DerivacionCdmCai, DerivacionSalud,
    DerivacionOfam, DerivacionDideco, DerivacionGestionTerritorial,
    DerivacionCapsUdla, DerivacionOln, DerivacionOtro,
)
from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm, MotivoIngresoForm,
    AspectosPsicologicosForm, RedesApoyoForm, PlanAccionForm,
    DerivacionCavdForm, DerivacionUravitForm, DerivacionCdmCaiForm,
    DerivacionSaludForm, DerivacionOfamForm, DerivacionDidecoForm,
    DerivacionGestionTerritorialForm, DerivacionCapsUdlaForm,
    DerivacionOlnForm, DerivacionOtroForm,
)

# Listado DRY de tuplas (nombre_campo, modelo, form, prefix)
DERIVS = [
    ('deriv_cavd', DerivacionCavd, DerivacionCavdForm, 'deriv_cavd'),
    ('deriv_uravit', DerivacionUravit, DerivacionUravitForm, 'deriv_uravit'),
    ('deriv_cdm_cai', DerivacionCdmCai, DerivacionCdmCaiForm, 'deriv_cdm_cai'),
    ('deriv_salud', DerivacionSalud, DerivacionSaludForm, 'deriv_salud'),
    ('deriv_ofam', DerivacionOfam, DerivacionOfamForm, 'deriv_ofam'),
    ('deriv_dideco', DerivacionDideco, DerivacionDidecoForm, 'deriv_dideco'),
    ('deriv_gestion_territorial', DerivacionGestionTerritorial, DerivacionGestionTerritorialForm, 'deriv_gestion_territorial'),
    ('deriv_caps_udla', DerivacionCapsUdla, DerivacionCapsUdlaForm, 'deriv_caps_udla'),
    ('deriv_oln', DerivacionOln, DerivacionOlnForm, 'deriv_oln'),
    ('deriv_otro', DerivacionOtro, DerivacionOtroForm, 'deriv_otro'),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ... tus imports de modelos y forms y DERIVS ...

@login_required
def editar_ficha(request, ficha_id):
    ficha = get_object_or_404(FichaAcogida, id=ficha_id)
    persona = getattr(ficha, "personaatendida", None)
    denuncia = getattr(ficha, "denuncia", None)
    motivo = getattr(ficha, "motivoingreso", None)
    psicologico = getattr(ficha, "aspectospsicologicos", None)
    redes = getattr(ficha, "redesapoyo", None)
    plan = getattr(ficha, "planaccion", None)

    derivs_instances = {
        campo: modelo.objects.filter(ficha=ficha).first()
        for campo, modelo, _, _ in DERIVS
    }

    if request.method == 'POST':
        form_ficha = FichaAcogidaForm(request.POST, instance=ficha, prefix='ficha')
        form_persona = PersonaAtendidaForm(request.POST, instance=persona, prefix='persona')
        form_denuncia = DenunciaForm(request.POST, instance=denuncia, prefix='denuncia')
        form_motivo = MotivoIngresoForm(request.POST, instance=motivo, prefix='motivo')
        form_psicologico = AspectosPsicologicosForm(request.POST, instance=psicologico, prefix='psico')
        form_redes = RedesApoyoForm(request.POST, instance=redes, prefix='redes')
        form_plan = PlanAccionForm(request.POST, instance=plan, prefix='plan')

        derivs_forms = {
            f'form_{campo}': form_class(request.POST, instance=derivs_instances[campo], prefix=prefix)
            for campo, _, form_class, prefix in DERIVS
        }

        all_valid = (
            form_ficha.is_valid() and form_persona.is_valid() and form_denuncia.is_valid()
            and form_motivo.is_valid() and form_psicologico.is_valid() and form_redes.is_valid()
            and form_plan.is_valid()
            and all(df.is_valid() for df in derivs_forms.values())
        )

        if all_valid:
            form_ficha.save()
            for form, obj, rel in [
                (form_persona, persona, 'personaatendida'),
                (form_denuncia, denuncia, 'denuncia'),
                (form_motivo, motivo, 'motivoingreso'),
                (form_psicologico, psicologico, 'aspectospsicologicos'),
                (form_redes, redes, 'redesapoyo'),
                (form_plan, plan, 'planaccion'),
            ]:
                instance = form.save(commit=False)
                instance.ficha = ficha
                instance.save()

            # Lógica de guardar/limpiar derivaciones según checkbox
            for campo, modelo, _, prefix in DERIVS:
                checkbox_name = f"{campo}-check"
                dform = derivs_forms[f'form_{campo}']
                deriv = derivs_instances[campo]
                if request.POST.get(checkbox_name):
                    # Guardar o actualizar si el checkbox está marcado
                    instance = dform.save(commit=False)
                    instance.ficha = ficha
                    instance.save()
                else:
                    # Si el checkbox NO está marcado y existe la derivación, elimínala
                    if deriv:
                        deriv.delete()

            messages.success(request, "Ficha actualizada correctamente.")
            return redirect('fichas:ver_ficha_completa', ficha.id)
    else:
        form_ficha = FichaAcogidaForm(instance=ficha, prefix='ficha')
        form_persona = PersonaAtendidaForm(instance=persona, prefix='persona')
        form_denuncia = DenunciaForm(instance=denuncia, prefix='denuncia')
        form_motivo = MotivoIngresoForm(instance=motivo, prefix='motivo')
        form_psicologico = AspectosPsicologicosForm(instance=psicologico, prefix='psico')
        form_redes = RedesApoyoForm(instance=redes, prefix='redes')
        form_plan = PlanAccionForm(instance=plan, prefix='plan')

        
        derivs_forms = {
            f'form_{campo}': form_class(instance=derivs_instances[campo], prefix=prefix)
            for campo, _, form_class, prefix in DERIVS
        }

    context = {
        'ficha': ficha,
        'form_ficha': form_ficha,
        'form_persona': form_persona,
        'form_denuncia': form_denuncia,
        'form_motivo': form_motivo,
        'form_psicologico': form_psicologico,
        'form_redes': form_redes,
        'form_plan': form_plan,
        **derivs_forms,
    }
    return render(request, 'fichas/editar_ficha.html', context)



from .models import (
    FichaAcogida,
    DerivacionCavd,
    DerivacionUravit,
    DerivacionCdmCai,
    DerivacionSalud,
    DerivacionOfam,
    DerivacionDideco,
    DerivacionGestionTerritorial,
    DerivacionCapsUdla,
    DerivacionOln,
    DerivacionOtro,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import (
    FichaAcogida,
    PersonaAtendida,
    Denuncia,
    MotivoIngreso,
    AspectosPsicologicos,
    RedesApoyo,
    PlanAccion,
    Egreso,
    Intervencion,
    DerivacionCavd,
    DerivacionUravit,
    DerivacionCdmCai,
    DerivacionSalud,
    DerivacionOfam,
    DerivacionDideco,
    DerivacionGestionTerritorial,
    DerivacionCapsUdla,
    DerivacionOln,
    DerivacionOtro,
)


@login_required
def ver_ficha_completa(request, ficha_id):
    # Obtengo la ficha o 404
    ficha = get_object_or_404(FichaAcogida, id=ficha_id)

    # Relaciones uno-a-uno
    persona     = getattr(ficha, 'personaatendida', None)
    denuncia    = getattr(ficha, 'denuncia', None)
    motivo      = getattr(ficha, 'motivoingreso', None)
    psicologico = getattr(ficha, 'aspectospsicologicos', None)
    redes       = getattr(ficha, 'redesapoyo', None)
    plan        = getattr(ficha, 'planaccion', None)
    egreso      = getattr(ficha, 'egreso', None)

    # Todas las intervenciones vinculadas, ordenadas por fecha
    intervenciones = Intervencion.objects.filter(ficha=ficha).order_by('fecha')

    # Derivaciones (OneToOneField en cada modelo)
    deriv_cavd               = getattr(ficha, 'derivacion_cavd', None)
    deriv_uravit             = getattr(ficha, 'derivacion_uravit', None)
    deriv_cdm_cai            = getattr(ficha, 'derivacion_cdm_cai', None)
    deriv_salud              = getattr(ficha, 'derivacion_salud', None)
    deriv_ofam               = getattr(ficha, 'derivacion_ofam', None)
    deriv_dideco             = getattr(ficha, 'derivacion_dideco', None)
    deriv_gestion_territorial= getattr(ficha, 'derivacion_gestion_territorial', None)
    deriv_caps_udla          = getattr(ficha, 'derivacion_caps_udla', None)
    deriv_oln                = getattr(ficha, 'derivacion_oln', None)
    deriv_otro               = getattr(ficha, 'derivacion_otro', None)

    context = {
        'ficha': ficha,
        'persona': persona,
        'denuncia': denuncia,
        'motivo': motivo,
        'psicologico': psicologico,
        'redes': redes,
        'plan': plan,
        'egreso': egreso,
        'intervenciones': intervenciones,
        # Paso cada derivación para que en el template puedas hacer {% if deriv_cavd %} … {% endif %}
        'deriv_cavd': deriv_cavd,
        'deriv_uravit': deriv_uravit,
        'deriv_cdm_cai': deriv_cdm_cai,
        'deriv_salud': deriv_salud,
        'deriv_ofam': deriv_ofam,
        'deriv_dideco': deriv_dideco,
        'deriv_gestion_territorial': deriv_gestion_territorial,
        'deriv_caps_udla': deriv_caps_udla,
        'deriv_oln': deriv_oln,
        'deriv_otro': deriv_otro,
    }
    return render(request, 'fichas/ver_ficha.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos, RedesApoyo, PlanAccion
from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm, MotivoIngresoForm,
    AspectosPsicologicosForm, RedesApoyoForm, PlanAccionForm
)

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from fichas.models import FichaAcogida

@login_required
def buscar_persona(request):
    fichas = FichaAcogida.objects.all().select_related('personaatendida', 'motivoingreso', 'egreso')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    numero_ficha = request.GET.get('numero_ficha')
    nombre = request.GET.get('nombre')
    rut = request.GET.get('rut')
    domicilio = request.GET.get('domicilio')
    
    delito = request.GET.get('delito')
    estado = request.GET.get('estado')
    ingreso = request.GET.get('ingreso')
    if ingreso == "con_ingreso":
        fichas = fichas.filter(ingreso_efectivo=True)
    elif ingreso == "sin_ingreso":
        fichas = fichas.filter(ingreso_efectivo=False)

    if fecha_inicio:
        fichas = fichas.filter(fecha_recepcion__gte=fecha_inicio)
    if fecha_fin:
        fichas = fichas.filter(fecha_recepcion__lte=fecha_fin)
    if numero_ficha:
        fichas = fichas.filter(id=numero_ficha)
    if nombre:
        fichas = fichas.filter(personaatendida__nombre__icontains=nombre)
    if delito:
        fichas = fichas.filter(motivoingreso__motivo_ingreso=delito)
    if estado == "ABIERTA":
        fichas = fichas.filter(egreso__isnull=True)
    elif estado == "CERRADA":
        fichas = fichas.filter(egreso__isnull=False)
    if rut:
        fichas = fichas.filter(personaatendida__rut_pasaporte__icontains=rut)
    if domicilio:
        fichas = fichas.filter(personaatendida__direccion__icontains=domicilio)

    # ORDENAMIENTO
    ordenar_por = request.GET.get('ordenar_por', 'id')
    sentido = request.GET.get('sentido', 'desc')
    if not sentido:
        sentido = 'desc' 
    
    campos_permitidos = {
        'id': 'id',
        'fecha_recepcion': 'fecha_recepcion',
        'nombre': 'personaatendida__nombre',
        'delito': 'motivoingreso__motivo_ingreso',
    }
    campo = campos_permitidos.get(ordenar_por, 'id')
    if sentido == 'desc':
        campo = '-' + campo
    fichas = fichas.order_by(campo)
    hoy = date.today()
    for ficha in fichas:
        ultima = ficha.intervencion_set.order_by('-fecha').first()
        ficha.fecha_ultima_intervencion = ultima.fecha if ultima else None
        ficha.destacar_intervencion = (
            ultima and (hoy - ultima.fecha).days > 14
        )

    # PAGINACIÓN
    paginator = Paginator(fichas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Agrega esto para pasar las opciones del select
    OPCIONES_MOTIVO = getattr(FichaAcogida, 'OPCIONES_MOTIVO', [
        ('FEMICIDIO', 'Femicidio'),
        ('PARRICIDIO', 'Parricidio'),
        ('SECUESTRO', 'Secuestro / Intento Secuestro'),
        ('DELITO_SEXUAL', 'Delito Sexual'),
        ('ROBO', 'Robo'),
        ('VIF', 'Violencia Intrafamiliar (VIF)'),
        ('SUSTRACCION', 'Sustracción de Menores'),
        ('HOMICIDIO', 'Homicidio / Cuasidelito de Homicidio'),
        ('BALACERAS', 'Balas Locas / Balaceras'),
        ('LESIONES', 'Lesiones'),
        ('ODIO', 'Crímenes de Odio'),
        ('AMENAZAS', 'Amenazas'),
        ('DAÑOS', 'Daños'),
        ('FALLECIMIENTO', 'Fallecimientos'),
        ('OTROS', 'Otros'),
    ])
    columnas = [
        ('id', 'N° Ficha'),
        ('fecha_recepcion', 'Fecha Recepción'),
        ('nombre', 'Nombre'),
        ('delito', 'Motivo/Delito'),
        ('id', 'N° Ficha'),
        ('fecha_recepcion', 'Fecha Recepción'),
        ('nombre', 'Nombre'),
        ('delito', 'Motivo/Delito'),
        ('estado', 'Estado'),
        ('ultima_intervencion', 'Últ. intervención'),        
      
    ]
    context = {
        'page_obj': page_obj,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'numero_ficha': numero_ficha,
        'nombre': nombre,
        'delito': delito,
        'ordenar_por': ordenar_por,
        'sentido': sentido,
        'request': request,
        'OPCIONES_MOTIVO': OPCIONES_MOTIVO,
        'columnas': columnas, # <-- esto es lo nuevo
        'estado': estado,
        'rut': rut,
        'domicilio': domicilio,
        'ingreso': ingreso,

    }
    return render(request, 'fichas/buscar_persona.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FichaAcogida, Intervencion
from .forms import IntervencionForm

@login_required
def ingresar_intervencion(request):
    ficha_id = request.GET.get('ficha_id')
    ficha = None
    intervenciones = []
    if ficha_id:
        ficha = get_object_or_404(FichaAcogida, pk=ficha_id)
        # Trae todas las intervenciones asociadas, ordenadas por fecha descendente
        intervenciones = Intervencion.objects.filter(ficha=ficha).order_by('-fecha')
    else:
        # Si por error no hay ficha, puedes redirigir a otra página o mostrar error
        return redirect('fichas:buscar_persona')
    
    # El formulario solo lo necesitas si quieres mostrar un form tradicional (no necesario si solo usas AJAX)
    form = IntervencionForm()

    columnas = [
        ('fecha', 'Fecha'),
        ('etapa', 'Etapa'),
        ('tipo_intervencion', 'Tipo de Atención'),
        ('responsables', 'Responsables/es'),
        ('participantes', 'Participantes'),
        ('lugar_via', 'Lugar o Vía de Intervención'),
        ('objetivos', 'Objetivo/s'),
        ('descripcion', 'Descripción'),
        ('resultados', 'Resultados/Sugerencias'),
    ]

    context = {
        'form': form,
        'ficha': ficha,
        'intervenciones': intervenciones,
        'columnas': columnas,  # Por si lo quieres usar en el template
    }
    return render(request, 'fichas/ingresar_intervencion.html', context)


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Intervencion, FichaAcogida

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from datetime import datetime

@csrf_exempt
@login_required
def api_intervencion_guardar(request, ficha_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
            ficha = FichaAcogida.objects.get(id=ficha_id)

            fecha_str = data.get("fecha")
            fecha_obj = None
            if fecha_str:
                try:
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except ValueError:
                    return JsonResponse({"success": False, "error": "Formato de fecha inválido"})

            interv = Intervencion.objects.create(
                ficha=ficha,
                fecha=fecha_obj,
                etapa=data.get("etapa"),
                tipo_intervencion=data.get("tipo_intervencion"),
                responsables=data.get("responsables", ""),
                participantes=data.get("participantes", ""),
                lugar_via=data.get("lugar_via"),
                objetivos=data.get("objetivos", ""),
                descripcion=data.get("descripcion", ""),
                resultados=data.get("resultados", ""),
                profesional=request.user,
            )
            return JsonResponse({
                "success": True,
                "id": interv.id,
                "fecha": interv.fecha.strftime("%Y-%m-%d") if interv.fecha else "",
                "etapa": interv.get_etapa_display(),
                "tipo_intervencion": interv.get_tipo_intervencion_display(),
                "responsables": interv.responsables,
                "participantes": interv.participantes,
                "lugar_via": interv.get_lugar_via_display(),
                "objetivos": interv.objetivos,
                "descripcion": interv.descripcion,
                "resultados": interv.resultados,

            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido"})


@csrf_exempt
@login_required
def api_intervencion_editar(request, intervencion_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
            interv = Intervencion.objects.get(id=intervencion_id)

            fecha_str = data.get("fecha")
            if fecha_str:
                try:
                    interv.fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except ValueError:
                    return JsonResponse({"success": False, "error": "Formato de fecha inválido"})

            interv.etapa = data.get("etapa")
            interv.tipo_intervencion = data.get("tipo_intervencion")
            interv.responsables = data.get("responsables", "")
            interv.participantes = data.get("participantes", "")
            interv.lugar_via = data.get("lugar_via")
            interv.objetivos = data.get("objetivos", "")
            interv.descripcion = data.get("descripcion", "")
            interv.resultados = data.get("resultados", "")
            interv.save()
            return JsonResponse({
                "success": True,
                "id": interv.id,
                "fecha": interv.fecha.strftime("%Y-%m-%d") if interv.fecha else "",
                "etapa": interv.get_etapa_display(),
                "tipo_intervencion": interv.get_tipo_intervencion_display(),
                "responsables": interv.responsables,
                "participantes": interv.participantes,
                "lugar_via": interv.get_lugar_via_display(),
                "objetivos": interv.objetivos,
                "descripcion": interv.descripcion,
                "resultados": interv.resultados,

            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required
def gestionar_egreso(request, ficha_id):
    ficha = get_object_or_404(FichaAcogida, id=ficha_id)
    # Busca el egreso existente o crea uno nuevo (sin guardar todavía)
    egreso = Egreso.objects.filter(ficha=ficha).first()
    if request.method == "POST":
        form = EgresoForm(request.POST, instance=egreso)
        if form.is_valid():
            nuevo_egreso = form.save(commit=False)
            nuevo_egreso.ficha = ficha   # <-- ASÍ asignas la ficha antes de guardar
            nuevo_egreso.save()
            return redirect('fichas:ver_ficha_completa', ficha.id)
    else:
        form = EgresoForm(instance=egreso)
    return render(request, 'fichas/gestionar_egreso.html', {
        'ficha': ficha,
        'form': form,
        'egreso': egreso,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import FichaAcogida, MotivoIngreso, PersonaAtendida, Intervencion, Barrio, Cuadrante

@login_required
def dashboard(request):
    # Filtros recibidos por GET
    barrio_id = request.GET.get('barrio')
    cuadrante_id = request.GET.get('cuadrante')
    genero = request.GET.get('genero')
    motivo = request.GET.get('motivo_ingreso')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    fichas = FichaAcogida.objects.all().select_related('personaatendida', 'motivoingreso')

    # Aplicar filtros
    if barrio_id:
        fichas = fichas.filter(personaatendida__barrio_id=barrio_id)
    if cuadrante_id:
        fichas = fichas.filter(personaatendida__cuadrante_id=cuadrante_id)
    if genero:
        fichas = fichas.filter(personaatendida__genero=genero)
    if motivo:
        fichas = fichas.filter(motivoingreso__motivo_ingreso=motivo)
    if fecha_inicio:
        fichas = fichas.filter(fecha_recepcion__gte=fecha_inicio)
    if fecha_fin:
        fichas = fichas.filter(fecha_recepcion__lte=fecha_fin)

    # Totales para cards
    total_fichas = fichas.count()
    total_intervenciones = Intervencion.objects.filter(ficha__in=fichas).count()
    total_egresos = fichas.filter(egreso__isnull=False).count()

    # Charts: Motivo de ingreso
    motivo_qs = fichas.values('motivoingreso__motivo_ingreso').annotate(cant=Count('id')).order_by('-cant')
    motivo_choices = dict(MotivoIngreso._meta.get_field('motivo_ingreso').choices)
    motivo_labels = [motivo_choices.get(m["motivoingreso__motivo_ingreso"], m["motivoingreso__motivo_ingreso"]) for m in motivo_qs]
    motivo_data = [m["cant"] for m in motivo_qs]

    # Charts: Género
    genero_qs = fichas.values('personaatendida__genero').annotate(cant=Count('id')).order_by('-cant')
    genero_choices = dict(PersonaAtendida._meta.get_field('genero').choices)
    genero_labels = [genero_choices.get(g["personaatendida__genero"], g["personaatendida__genero"]) for g in genero_qs]
    genero_data = [g["cant"] for g in genero_qs]

    # Charts: Barrio
    barrio_qs = fichas.values('personaatendida__barrio__nombre').annotate(cant=Count('id')).order_by('-cant')
    barrio_labels = [b["personaatendida__barrio__nombre"] or "Sin barrio" for b in barrio_qs]
    barrio_data = [b["cant"] for b in barrio_qs]

    # Filtros para selects
    barrios = Barrio.objects.all()
    cuadrantes = Cuadrante.objects.all()
    motivos = MotivoIngreso._meta.get_field('motivo_ingreso').choices
    generos = PersonaAtendida._meta.get_field('genero').choices

    context = {
        "total_fichas": total_fichas,
        "total_intervenciones": total_intervenciones,
        "total_egresos": total_egresos,
        "motivo_labels": motivo_labels,
        "motivo_data": motivo_data,
        "genero_labels": genero_labels,
        "genero_data": genero_data,
        "barrio_labels": barrio_labels,
        "barrio_data": barrio_data,
        "barrios": barrios,
        "cuadrantes": cuadrantes,
        "motivos": motivos,
        "generos": generos,
        "filtros": {
            "barrio": barrio_id,
            "cuadrante": cuadrante_id,
            "genero": genero,
            "motivo": motivo,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
    }
    return render(request, "fichas/dashboard.html", context)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
@login_required
def api_intervencion_eliminar(request, intervencion_id):
    if request.method == "POST":
        try:
            from .models import Intervencion
            interv = Intervencion.objects.get(id=intervencion_id)
            interv.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido"})


from .models import (
    FichaAcogida, PersonaAtendida, DerivacionCavd, DerivacionUravit, DerivacionCdmCai,
    DerivacionSalud, DerivacionOfam, DerivacionDideco, DerivacionGestionTerritorial,
    DerivacionCapsUdla, DerivacionOln, DerivacionOtro
)
from django.db.models import Q

DERIVACION_MODELS = [
    ('CAVD', DerivacionCavd, 'fecha_derivacion_cavd', 'fecha_respuesta_cavd', 'fecha_ingreso_cavd'),
    ('URAVIT', DerivacionUravit, 'fecha_derivacion_uravit', 'fecha_respuesta_uravit', None),
    ('CDM-CAI', DerivacionCdmCai, 'fecha_derivacion_cdm_cai', 'fecha_respuesta_cdm_cai', 'fecha_ingreso_cdm_cai'),
    ('SALUD', DerivacionSalud, 'fecha_derivacion_salud', 'fecha_respuesta_salud', 'fecha_ingreso_salud'),
    ('OFAM', DerivacionOfam, 'fecha_derivacion_ofam', 'fecha_respuesta_ofam', 'fecha_ingreso_ofam'),
    ('DIDECO', DerivacionDideco, 'fecha_derivacion_dideco', 'fecha_respuesta_dideco', 'fecha_ingreso_dideco'),
    ('GESTIÓN TERRITORIAL', DerivacionGestionTerritorial, 'fecha_derivacion_gestion_territorial', 'fecha_respuesta_gestion_territorial', 'fecha_ingreso_gestion_territorial'),
    ('CAPS UDLA', DerivacionCapsUdla, 'fecha_derivacion_caps_udla', 'fecha_respuesta_caps_udla', 'fecha_ingreso_caps_udla'),
    ('OLN', DerivacionOln, 'fecha_derivacion_oln', 'fecha_respuesta_oln', 'fecha_ingreso_oln'),
    ('OTRO', DerivacionOtro, 'fecha_derivacion_otro', 'fecha_respuesta_otro', 'fecha_ingreso_otro'),
]
from django.db.models import Q
from datetime import datetime, date
from .models import FichaAcogida, PersonaAtendida
from .forms import BuscarDerivacionForm  # lo crearás más abajo

from datetime import datetime

@login_required
def buscar_derivacion(request):
    derivaciones = []

    for nombre, modelo, campo_der, campo_resp, campo_ing in DERIVACION_MODELS:
        for obj in modelo.objects.select_related('ficha__personaatendida').all():
            derivaciones.append({
                'nombre': nombre,
                'ficha': obj.ficha,
                'persona': obj.ficha.personaatendida,
                'fecha_recepcion': obj.ficha.fecha_recepcion,
                'fecha_derivacion': getattr(obj, campo_der, None),
                'fecha_respuesta': getattr(obj, campo_resp, None),
                'fecha_ingreso': getattr(obj, campo_ing, None) if campo_ing else None,
            })

    form = BuscarDerivacionForm(request.GET or None)
    if form.is_valid():
        cd = form.cleaned_data

        if cd.get('nombre'):
            derivaciones = [
                d for d in derivaciones
                if d['persona'].nombre and cd['nombre'].lower() in d['persona'].nombre.lower()
            ]

        if cd.get('rut'):
            derivaciones = [
                d for d in derivaciones
                if d['persona'].rut_pasaporte and cd['rut'].lower() in d['persona'].rut_pasaporte.lower()
            ]

        if cd.get('tipo_derivacion'):
            derivaciones = [
                d for d in derivaciones
                if cd['tipo_derivacion'].lower() in d['nombre'].lower()
            ]

        if cd.get('fecha_inicio'):
            derivaciones = [
                d for d in derivaciones
                if d['fecha_derivacion'] and d['fecha_derivacion'] >= cd['fecha_inicio']
            ]

        if cd.get('fecha_fin'):
            derivaciones = [
                d for d in derivaciones
                if d['fecha_derivacion'] and d['fecha_derivacion'] <= cd['fecha_fin']
            ]

        if cd.get('solo_con_ingreso'):
            derivaciones = [
                d for d in derivaciones
                if d['fecha_ingreso'] is not None
            ]
        if cd.get('solo_con_derivacion'):
            derivaciones = [
                d for d in derivaciones
                if d['fecha_derivacion'] is not None
            ]
        if cd.get('solo_con_recepcion'):
            derivaciones = [
                d for d in derivaciones
                if d['ficha'].fecha_recepcion is not None
            ]

        if cd.get('solo_con_respuesta'):
            derivaciones = [
                d for d in derivaciones
                if d['fecha_respuesta'] is not None
            ]

    # Ordenar por N° ficha (id) descendente
    derivaciones = sorted(derivaciones, key=lambda x: x['ficha'].id if x['ficha'] else 0, reverse=True)
    # Filtros por fechas vacías
    if request.GET.get('sin_derivacion'):
        derivaciones = [d for d in derivaciones if not d['fecha_derivacion']]

    if request.GET.get('sin_respuesta'):
        derivaciones = [d for d in derivaciones if not d['fecha_respuesta']]

    if request.GET.get('sin_ingreso'):
        derivaciones = [d for d in derivaciones if not d['fecha_ingreso']]

    return render(request, 'fichas/buscar_derivacion.html', {
        'form': form,
        'derivaciones': derivaciones,
    })


