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


@login_required
def crear_ficha_completa(request):
    if request.method == 'POST':
        form_ficha = FichaAcogidaForm(request.POST)
        form_persona = PersonaAtendidaForm(request.POST)
        form_denuncia = DenunciaForm(request.POST)
        form_motivo = MotivoIngresoForm(request.POST)
        form_psicologico = AspectosPsicologicosForm(request.POST)
        form_redes = RedesApoyoForm(request.POST)
        form_plan = PlanAccionForm(request.POST)

        if all([
            form_ficha.is_valid(),
            form_persona.is_valid(),
            form_denuncia.is_valid(),
            form_motivo.is_valid(),
            form_psicologico.is_valid(),
            form_redes.is_valid(),
            form_plan.is_valid()
        ]):
            ficha = form_ficha.save(commit=False)
            ficha.profesional = request.user    # <--- ESTO es lo que evita el error
            ficha.save()

            persona = form_persona.save(commit=False)
            persona.ficha = ficha
            persona.save()

            denuncia = form_denuncia.save(commit=False)
            denuncia.ficha = ficha
            denuncia.save()

            motivo = form_motivo.save(commit=False)
            motivo.ficha = ficha
            motivo.save()

            psicologico = form_psicologico.save(commit=False)
            psicologico.ficha = ficha
            psicologico.save()

            redes = form_redes.save(commit=False)
            redes.ficha = ficha
            redes.save()

            plan = form_plan.save(commit=False)
            plan.ficha = ficha
            plan.save()

            return redirect(f'{reverse("fichas:ver_ficha_completa", args=[ficha.id])}?guardado=1')
    else:
        form_ficha = FichaAcogidaForm()
        form_persona = PersonaAtendidaForm()
        form_denuncia = DenunciaForm()
        form_motivo = MotivoIngresoForm()
        form_psicologico = AspectosPsicologicosForm()
        form_redes = RedesApoyoForm()
        form_plan = PlanAccionForm()

    return render(request, 'fichas/ficha_completa.html', {
        'form_ficha': form_ficha,
        'form_persona': form_persona,
        'form_denuncia': form_denuncia,
        'form_motivo': form_motivo,
        'form_psicologico': form_psicologico,
        'form_redes': form_redes,
        'form_plan': form_plan,
        'persona': form_persona.instance,
    })


@login_required
def ver_ficha_completa(request, ficha_id):
    ficha = get_object_or_404(FichaAcogida, id=ficha_id)
    persona = getattr(ficha, 'personaatendida', None)
    denuncia = getattr(ficha, 'denuncia', None)
    motivo = getattr(ficha, 'motivoingreso', None)
    psicologico = getattr(ficha, 'aspectospsicologicos', None)
    redes = getattr(ficha, 'redesapoyo', None)
    plan = getattr(ficha, 'planaccion', None)

    context = {
        'ficha': ficha,
        'persona': persona,
        'denuncia': denuncia,
        'motivo': motivo,
        'psicologico': psicologico,
        'redes': redes,
        'plan': plan,        
    }
    return render(request, 'fichas/ver_ficha.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso, AspectosPsicologicos, RedesApoyo, PlanAccion
from .forms import (
    FichaAcogidaForm, PersonaAtendidaForm, DenunciaForm, MotivoIngresoForm,
    AspectosPsicologicosForm, RedesApoyoForm, PlanAccionForm
)

@login_required
def editar_ficha_completa(request, ficha_id):
    ficha = get_object_or_404(FichaAcogida, id=ficha_id)
    persona = getattr(ficha, 'personaatendida', None)
    denuncia = getattr(ficha, 'denuncia', None)
    motivo = getattr(ficha, 'motivoingreso', None)
    psicologico = getattr(ficha, 'aspectospsicologicos', None)
    redes = getattr(ficha, 'redesapoyo', None)
    plan = getattr(ficha, 'planaccion', None)

    if request.method == 'POST':
        form_ficha = FichaAcogidaForm(request.POST, instance=ficha)
        form_persona = PersonaAtendidaForm(request.POST, instance=persona)
        form_denuncia = DenunciaForm(request.POST, instance=denuncia)
        form_motivo = MotivoIngresoForm(request.POST, instance=motivo)
        form_psicologico = AspectosPsicologicosForm(request.POST, instance=psicologico)
        form_redes = RedesApoyoForm(request.POST, instance=redes)
        form_plan = PlanAccionForm(request.POST, instance=plan)

        # Relacionar las instancias correctamente antes de guardar
        if form_ficha.is_valid() and form_persona.is_valid() and form_denuncia.is_valid() \
            and form_motivo.is_valid() and form_psicologico.is_valid() and form_redes.is_valid() and form_plan.is_valid():
            
            ficha = form_ficha.save()
            persona = form_persona.save(commit=False)
            denuncia = form_denuncia.save(commit=False)
            motivo = form_motivo.save(commit=False)
            psicologico = form_psicologico.save(commit=False)
            redes = form_redes.save(commit=False)
            plan = form_plan.save(commit=False)
            
            # Relacionar con ficha si corresponde
            persona.ficha = ficha
            denuncia.ficha = ficha
            motivo.ficha = ficha
            psicologico.ficha = ficha
            redes.ficha = ficha
            plan.ficha = ficha
            
            persona.save()
            denuncia.save()
            motivo.save()
            psicologico.save()
            redes.save()
            plan.save()
            return redirect('fichas:ver_ficha_completa', ficha.id)
    else:
        form_ficha = FichaAcogidaForm(instance=ficha)
        form_persona = PersonaAtendidaForm(instance=persona)
        form_denuncia = DenunciaForm(instance=denuncia)
        form_motivo = MotivoIngresoForm(instance=motivo)
        form_psicologico = AspectosPsicologicosForm(instance=psicologico)
        form_redes = RedesApoyoForm(instance=redes)
        form_plan = PlanAccionForm(instance=plan)

    return render(request, 'fichas/editar_ficha.html', {
        'form_ficha': form_ficha,
        'form_persona': form_persona,
        'form_denuncia': form_denuncia,
        'form_motivo': form_motivo,
        'form_psicologico': form_psicologico,
        'form_redes': form_redes,
        'form_plan': form_plan,
        'ficha': ficha,
    })

    
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from fichas.models import FichaAcogida

@login_required
def buscar_persona(request):
    fichas = FichaAcogida.objects.all().select_related('personaatendida', 'motivoingreso')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    numero_ficha = request.GET.get('numero_ficha')
    nombre = request.GET.get('nombre')
    delito = request.GET.get('delito')

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
        ('delito', 'Motivo/Delito')
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
                profesional=request.user
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
