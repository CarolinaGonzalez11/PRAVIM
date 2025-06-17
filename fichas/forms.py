from django import forms
from datetime import date
from fichas.models import (
    FichaAcogida, PersonaAtendida, Denuncia, MotivoIngreso,
    AspectosPsicologicos, RedesApoyo, Egreso, Intervencion
)




# Validación para fechas posteriores a 2025
def validar_fecha_2025(value):
    if value and value.year < 2025:
        raise forms.ValidationError("La fecha debe ser posterior al año 2025.")
    return value

PROFESIONALES_UAV = [
    ('NATHALY REYES', 'Nathaly Reyes'),
    ('PALOMA QUINTEROS', 'Paloma Quinteros'),
    ('GLORIA RIVERA', 'Gloria Rivera'),
]

class FichaAcogidaForm(forms.ModelForm):
    profesionales_contacto_1 = forms.MultipleChoiceField(
        choices=PROFESIONALES_UAV,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Profesionales en primer contacto"
    )
    ingreso_efectivo = forms.TypedChoiceField(
        label="¿Ingreso efectivo?",
        choices=[(True, "Sí"), (False, "No")],
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect,
        required=False,
    )
    contencion_inicial = forms.TypedChoiceField(
        label="¿Recibió contención inicial?",
        choices=[(True, "Sí"), (False, "No")],
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect,
        required=False,
    )    
    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('fecha_recepcion'):
            self.add_error('fecha_recepcion', "Debes ingresar la fecha de recepción.")
        return cleaned
    class Meta:
        model = FichaAcogida
        exclude = ['profesional']
        fields = '__all__'
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_contacto_1': forms.DateInput(attrs={'type': 'date'}),
            'fecha_contacto_2': forms.DateInput(attrs={'type': 'date'}),
            'fecha_contacto_3': forms.DateInput(attrs={'type': 'date'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
    
    def clean_fecha_recepcion(self):
        return validar_fecha_2025(self.cleaned_data.get('fecha_recepcion'))

    def clean_fecha_contacto_1(self):
        return validar_fecha_2025(self.cleaned_data.get('fecha_contacto_1'))

    def clean_fecha_contacto_2(self):
        return validar_fecha_2025(self.cleaned_data.get('fecha_contacto_2'))

    def clean_fecha_contacto_3(self):
        return validar_fecha_2025(self.cleaned_data.get('fecha_contacto_3'))

NACIONALIDADES_FRECUENTES = [
    ('', '---------'),
    ('Chile', 'Chilena'),
    ('Venezuela', 'Venezolana'),
    ('Perú', 'Peruana'),
    ('Colombia', 'Colombiana'),
    ('Haití', 'Haitiana'),
    ('Bolivia', 'Boliviana'),
    ('Argentina', 'Argentina'),
    ('Ecuador', 'Ecuatoriana'),
    ('R. Dominicana', 'Dominicana'),
    ('Cuba', 'Cubana'),
    ('Brasil', 'Brasileña'),
    ('España', 'Española'),
    ('China', 'China'),
    ('Estados Unidos', 'Estadounidense'),
    ('México', 'Mexicana'),
    ('Alemania', 'Alemana'),
    ('Francia', 'Francesa'),
    ('Paraguay', 'Paraguaya'),
    ('Uruguay', 'Uruguaya'),
    ('Italia', 'Italiana'),
    ('Otro', 'Otro'),
]

# Listado de CESFAM (igual que en tu modelo)
CESFAM_CHOICES = [
    ('', '---------'),
    ('CESFAM Maipú (Pajaritos)', 'CESFAM Maipú (Pajaritos)'),
    ('CESFAM Dra. Ana María Juricic', 'CESFAM Dra. Ana María Juricic'),
    ('CESFAM Dr. Eduardo Ahués', 'CESFAM Dr. Eduardo Ahués'),
    ('CESFAM Dr. Carlos Godoy', 'CESFAM Dr. Carlos Godoy'),
    ('CESFAM Dr. Iván Insunza', 'CESFAM Dr. Iván Insunza'),
    ('CESFAM Clotario Blest', 'CESFAM Clotario Blest'),
    ('CESFAM Presidenta Michelle Bachelet', 'CESFAM Presidenta Michelle Bachelet'),
    ('CESFAM Dr. Luis Ferrada', 'CESFAM Dr. Luis Ferrada'),
    ('CESFAM Dr. Salvador Allende (El Abrazo)', 'CESFAM Dr. Salvador Allende (El Abrazo)'),
    ('OTRO', 'Otro (especifique)'),
]

RANGO_ETAREO_CHOICES = [
    ('', '---------'),
    ('0-14', '0-14 años'),
    ('15-17', '15-17 años'),
    ('18-30', '18-30 años'),
    ('31-40', '31-40 años'),
    ('41-59', '41-59 años'),
    ('60+', '60 años o más'),
]


class PersonaAtendidaForm(forms.ModelForm):
    # CESFAM Dropdown + otro
    cesfam = forms.ChoiceField(
        choices=CESFAM_CHOICES,
        required=False,
        label="CESFAM Vinculante",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_cesfam'})
    )
    cesfam_otro = forms.CharField(
        required=False,
        label="Otro CESFAM",
        widget=forms.TextInput(attrs={'placeholder': 'Especifique CESFAM', 'id': 'id_cesfam_otro'})
    )

    # Nacionalidad Dropdown + otro
    nacionalidad = forms.ChoiceField(
        choices=NACIONALIDADES_FRECUENTES,
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione o busque nacionalidad',
            'id': 'id_nacionalidad',
        }),
        required=False,
        label='Nacionalidad'
    )
    nacionalidad_otro = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Especifique nacionalidad', 'id': 'id_nacionalidad_otro'}),
        label='Otra nacionalidad'
    )

    # Género Otro
    genero_otro = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Especifique género', 'id': 'id_genero_otro'}),
        label='Otro género'
    )

    # Rango etáreo (solo editable si no hay fecha de nacimiento)
    rango_etareo = forms.ChoiceField(
        choices=RANGO_ETAREO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_rango_etareo'}),
        label='Rango etáreo'
    )

    class Meta:
        model = PersonaAtendida
        exclude = ['edad']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODOS los campos opcionales por defecto
        for field in self.fields.values():
            field.required = False

        # Rango etáreo: solo editable si no hay fecha_nacimiento
        fecha = self.initial.get('fecha_nacimiento') or self.data.get('fecha_nacimiento')
        if fecha:
            self.fields['rango_etareo'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['rango_etareo'].widget.attrs.pop('disabled', None)

    def clean(self):
        cleaned = super().clean()
        # Género Otro
        if cleaned.get('genero') == 'OTRO' and not cleaned.get('genero_otro', '').strip():
            self.add_error('genero_otro', "Debes especificar el género si seleccionas 'Otro'.")
        # Nacionalidad Otro
        if cleaned.get('nacionalidad') == 'Otro' and not cleaned.get('nacionalidad_otro', '').strip():
            self.add_error('nacionalidad_otro', "Debes especificar la nacionalidad si seleccionas 'Otro'.")
        # CESFAM Otro
        if cleaned.get('cesfam') == 'OTRO' and not cleaned.get('cesfam_otro', '').strip():
            self.add_error('cesfam_otro', "Debes especificar el CESFAM si seleccionas 'Otro'.")
        return cleaned

class DenunciaForm(forms.ModelForm):
    DIFICULTADES_CHOICES = [
        ('mal_trato', 'Mal trato/trato inadecuado'),
        ('tiempo_espera', 'Tiempo de espera'),
        ('no_llegaron', 'No llegaron a llamado'),
        ('otra', 'Otra'),
    ]
    dificultades = forms.ChoiceField(
        choices=DIFICULTADES_CHOICES,
        widget=forms.RadioSelect,   # O Select
        required=False,
        label='Dificultades'
    )

    class Meta:
        model = Denuncia
        fields = [
            'tiene_denuncia', 'anio_denuncia', 'lugar_denuncia', 'lugar_denuncia_otro',
            'numero_causa', 'motivo_denuncia',
            'dificultades', 'dificultades_otra',
            'medida_cautelar', 'medida_cautelar_detalle'
        ]
        widgets = {
            'anio_denuncia': forms.TextInput(attrs={'placeholder': 'Ej: 2025'}),
            'motivo_denuncia': forms.Textarea(attrs={'rows': 2}),
            'dificultades_otra': forms.Textarea(attrs={'rows': 2}),
            'medida_cautelar_detalle': forms.TextInput(attrs={'placeholder': 'Ej: Prohibición de acercamiento'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('dificultades') == 'otra' and not cleaned.get('dificultades_otra', '').strip():
            self.add_error('dificultades_otra', "Debes especificar la dificultad si seleccionas 'Otra'.")
        return cleaned

class MotivoIngresoForm(forms.ModelForm):
    class Meta:
        model = MotivoIngreso
        fields = '__all__'
        exclude = ['ficha']
        help_texts = {
            'motivo_otro': 'Por favor, especifica el motivo si seleccionaste "Otro".'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Todos los campos opcionales por defecto

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('motivo_ingreso'):
            self.add_error('motivo_ingreso', "Debes ingresar el motivo principal de ingreso.")
        if cleaned.get('motivo_ingreso') == 'OTROS' and not cleaned.get('motivo_otro', '').strip():
            self.add_error('motivo_otro', "Debes especificar el motivo si seleccionas 'Otro'.")
        return cleaned
    
from django import forms
from .models import AspectosPsicologicos

# Choices auxiliares (puedes importarlos desde tu models.py si los tienes ahí)
ACTITUD_CHOICES = [
    ('Colaboradora', 'Colaboradora'),
    ('Reticente', 'Reticente'),
    ('Querellante', 'Querellante'),
    ('Agresiva', 'Agresiva'),
    ('Inhibida', 'Inhibida'),
]

LENGUAJE_CHOICES = [
    ('Verborreico', 'Verborreico'),
    ('Mutismo', 'Mutismo'),
    ('Neologismos', 'Neologismos'),
]

AFECTIVIDAD_CHOICES = [
    ('Humor expansivo', 'Humor expansivo'),
    ('Humor deprimido', 'Humor deprimido'),
    ('Indiferencia_afectiva', 'Indiferencia afectiva'),
    ('Labilidad', 'Labilidad'),
]

SUENO_CHOICES = [
    ('Insomnio', 'Insomnio'),
    ('Hipersomnia', 'Hipersomnia'),
]

ALIMENTACION_CHOICES = [
    ('Anorexia', 'Anorexia'),
    ('Negativa a comer', 'Negativa a comer'),
    ('Hiporexia', 'Hiporexia'),
]

LIMITACION_CHOICES = [
    ('No puede salir', 'No puede salir'),
    ('No puede realizar actividades', 'No puede realizar actividades habituales'),
]

ESTADO_CONCIENCIA_CHOICES = [
    ('Lúcido', 'Lúcido'),
    ('Obnubilado', 'Obnubilado'),
]

ORIENTACION_CHOICES = [
    ('Desorientacion temporal', 'Desorientación temporal'),
    ('Desorientacion espacial', 'Desorientación espacial'),
]

ESTADO_COGNITIVO_CHOICES = [
    ('Problemas de atención', 'Problemas de atención'),
    ('Problemas de concentración', 'Problemas de concentración'),
    ('Problemas de memoria', 'Problemas de memoria'),
]

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

class AspectosPsicologicosForm(forms.ModelForm):
    # Campos principales
    antecedentes = forms.CharField(
        required=False,
        label="Antecedentes (campo de texto libre)",
        widget=forms.Textarea(attrs={'rows': 2})
    )
    diagnostico = forms.ChoiceField(
        choices=[('', '---------')] + DIAGNOSTICO_CHOICES,
        required=False,
        label="Diagnóstico"
    )

    diagnostico_otro = forms.CharField(
        required=False,
        label="Otro diagnóstico (especifique)",
        widget=forms.TextInput(attrs={'placeholder': 'Especifique si seleccionó Otro'})
    )

    atencion_salud_mental = forms.BooleanField(
        required=False,
        label="¿Ha tenido atención en salud mental?"
    )
    atencion_anio = forms.CharField(
        required=False,
        label="Año de atención",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 2024'})
    )
    atencion_lugar = forms.CharField(
        required=False,
        label="Lugar de atención",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: CESFAM, COSAM, etc.'})
    )

    internacion = forms.BooleanField(
        required=False,
        label="¿Ha tenido internaciones?"
    )
    internacion_anio = forms.CharField(
        required=False,
        label="Año de internación",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 2024'})
    )
    internacion_lugar = forms.CharField(
        required=False,
        label="Lugar de internación",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Hospital, COSAM, etc.'})
    )

    afectacion_psicologica = forms.CharField(
        required=False,
        label="Ideación y/o intentos suicidas  ( año, motivo, otros, especifique) ",
        widget=forms.Textarea(attrs={'rows': 2})
    )

    # Campos multiselección
    estado_conciencia = forms.MultipleChoiceField(
        choices=ESTADO_CONCIENCIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    orientacion = forms.MultipleChoiceField(
        choices=ORIENTACION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    estado_cognitivo = forms.MultipleChoiceField(
        choices=ESTADO_COGNITIVO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    actitud = forms.MultipleChoiceField(
        choices=ACTITUD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    lenguaje = forms.MultipleChoiceField(
        choices=LENGUAJE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    afectividad = forms.MultipleChoiceField(
        choices=AFECTIVIDAD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sueno = forms.MultipleChoiceField(
        choices=SUENO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    alimentacion = forms.MultipleChoiceField(
        choices=ALIMENTACION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    limitacion_vida_cotidiana = forms.MultipleChoiceField(
        choices=LIMITACION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = AspectosPsicologicos
        exclude = ['ficha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Todos los campos opcionales

    def clean(self):
        cleaned = super().clean()
        # Validar diagnóstico otro (esto sí tiene sentido mantener)
        if cleaned.get('diagnostico') == 'otro' and not cleaned.get('diagnostico_otro'):
            self.add_error('diagnostico_otro', "Debes especificar el diagnóstico si seleccionas 'Otro'.")
        # NO más validaciones de año/lugar, todo opcional
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Guardar campos multiseleccionables como JSON
        instance.estado_conciencia = self.cleaned_data.get('estado_conciencia', [])
        instance.orientacion = self.cleaned_data.get('orientacion', [])
        instance.estado_cognitivo = self.cleaned_data.get('estado_cognitivo', [])
        instance.actitud = self.cleaned_data.get('actitud', [])
        instance.lenguaje = self.cleaned_data.get('lenguaje', [])
        instance.afectividad = self.cleaned_data.get('afectividad', [])
        instance.sueno = self.cleaned_data.get('sueno', [])
        instance.alimentacion = self.cleaned_data.get('alimentacion', [])
        instance.limitacion_vida_cotidiana = self.cleaned_data.get('limitacion_vida_cotidiana', [])
        if commit:
            instance.save()
        return instance


        
class RedesApoyoForm(forms.ModelForm):
    class Meta:
        model = RedesApoyo
        fields = '__all__'
        exclude = ['ficha'] 
        
class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = '__all__'
        exclude = ['ficha'] 
        widgets = {
            'fecha_egreso': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_fecha_egreso(self):
        return validar_fecha_2025(self.cleaned_data.get('fecha_egreso'))

class IntervencionForm(forms.ModelForm):
    class Meta:
        model = Intervencion
        exclude = ['ficha', 'profesional']  # si se asigna automáticamente en la vista
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción...'}),
            'responsables': forms.CheckboxSelectMultiple,
            'objetivos': forms.CheckboxSelectMultiple,
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción...'}),
            'resultados': forms.TextInput(attrs={'placeholder': 'Resultados o sugerencias...'}),
        }      
      
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def clean_fecha(self):
        return validar_fecha_2025(self.cleaned_data.get('fecha'))

from .models import PlanAccion

class PlanAccionForm(forms.ModelForm):
    class Meta:
        model = PlanAccion
        exclude = ['ficha']
        widgets = {
            # UAV Psicológica y Social (igual que tenías)
            'uav_psicologica_1_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_psicologica_2_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_psicologica_3_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_social_1_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_social_2_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_social_3_detalle': forms.Textarea(attrs={'rows': 2}),
            # UAV Legal
            'uav_legal_1_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_legal_2_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_legal_3_detalle': forms.Textarea(attrs={'rows': 2}),
            # Patrullaje
            'registro_patrullaje': forms.TextInput(attrs={'placeholder': 'Ej: 2025-0001'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # todos opcionales

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
from django import forms
from .models import (
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

class DerivacionBaseForm(forms.ModelForm):
    """
    Formulario base para derivaciones: todos los campos opcionales,
    y la relación con la ficha oculta en un HiddenInput.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fld in self.fields.values():
            fld.required = False

    class Meta:
        fields = '__all__'
        widgets = {
            'ficha': forms.HiddenInput(),
        }

class DerivacionCavdForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionCavd
        fields = [f.name for f in DerivacionCavd._meta.fields if f.name not in ('id','ficha')]
        labels = {
            'descripcion_cavd': 'Descripción (CAVD)',
            'fecha_derivacion_cavd': 'Fecha de derivación',
            'es_vinculacion_cavd': 'Es vinculación',
            'fecha_respuesta_cavd': 'Fecha de respuesta',
            'ingresa_cavd': 'Ingresa al programa',
            'fecha_ingreso_cavd': 'Fecha de ingreso',
            'es_conmocion_publica_cavd': 'Conmoción pública',
            'fecha_vinculacion_conmocion_cavd': 'Fecha vinculación conmoción',
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_cavd': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_cavd': forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_cavd':   forms.DateInput(attrs={'type':'date'}),
            'fecha_vinculacion_conmocion_cavd': forms.DateInput(attrs={'type':'date'}),
        }

class DerivacionUravitForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionUravit
        fields = [f.name for f in DerivacionUravit._meta.fields if f.name not in ('id','ficha')]
        labels = {
            'descripcion_uravit': 'Descripción (URAVIT)',
            'fecha_derivacion_uravit': 'Fecha de derivación',
            'es_vinculacion_uravit': 'Es vinculación',
            'fecha_respuesta_uravit': 'Fecha de respuesta',
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_uravit': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_uravit':  forms.DateInput(attrs={'type':'date'}),
        }

class DerivacionCdmCaiForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionCdmCai
        fields = [f.name for f in DerivacionCdmCai._meta.fields if f.name not in ('id','ficha')]
        labels = {
            'descripcion_cdm_cai': 'Descripción (CDM-CAI)',
            'fecha_derivacion_cdm_cai': 'Fecha de derivación',
            'es_vinculacion_cdm_cai': 'Es vinculación',
            'fecha_respuesta_cdm_cai': 'Fecha de respuesta',
            'ingresa_cdm_cai': 'Ingresa al programa',
            'fecha_ingreso_cdm_cai': 'Fecha de ingreso',
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_cdm_cai': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_cdm_cai':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_cdm_cai':    forms.DateInput(attrs={'type':'date'}),
        }


class DerivacionSaludForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionSalud
        fields = [f.name for f in DerivacionSalud._meta.fields if f.name not in ('id','ficha')]
        labels = {
            'dispositivo_salud': 'Dispositivo de salud',
            'fecha_derivacion_salud': 'Fecha de derivación',
            'es_vinculacion_salud': 'Es vinculación',
            'fecha_respuesta_salud': 'Fecha de respuesta',
            'ingresa_salud': 'Ingresa al dispositivo',
            'fecha_ingreso_salud': 'Fecha de ingreso',
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_salud': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_salud':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_salud':    forms.DateInput(attrs={'type':'date'}),
        }
        def clean(self):
            cleaned_data = super().clean()
            dispositivo = cleaned_data.get('dispositivo_salud')
            otro = cleaned_data.get('dispositivo_salud_otro')
            if dispositivo == 'OTRO' and not otro:
                self.add_error('dispositivo_salud_otro', 'Debe especificar el dispositivo de salud.')
            return cleaned_data


class DerivacionOfamForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionOfam
        fields = [f.name for f in DerivacionOfam._meta.fields if f.name not in ('id','ficha')]
        labels = {
            f.name: f.name.replace('_ofam','').replace('_',' ').capitalize()
            for f in DerivacionOfam._meta.fields
            if f.name not in ('id','ficha')
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_ofam': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_ofam':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_ofam':    forms.DateInput(attrs={'type':'date'}),
        }

class DerivacionDidecoForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionDideco
        fields = [f.name for f in DerivacionDideco._meta.fields if f.name not in ('id','ficha')]
        labels = {
            f.name: f.name.replace('_dideco','').replace('_',' ').capitalize()
            for f in DerivacionDideco._meta.fields
            if f.name not in ('id','ficha')
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_dideco': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_dideco':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_dideco':    forms.DateInput(attrs={'type':'date'}),
        }

class DerivacionGestionTerritorialForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionGestionTerritorial
        fields = [f.name for f in DerivacionGestionTerritorial._meta.fields if f.name not in ('id','ficha')]
        labels = {
            f.name: f.name.replace('_gestion_territorial','').replace('_',' ').capitalize()
            for f in DerivacionGestionTerritorial._meta.fields
            if f.name not in ('id','ficha')
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_gestion_territorial': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_gestion_territorial':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_gestion_territorial':    forms.DateInput(attrs={'type':'date'}),
        }


class DerivacionCapsUdlaForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionCapsUdla
        fields = [f.name for f in DerivacionCapsUdla._meta.fields if f.name not in ('id','ficha')]
        labels = {
            f.name: f.name.replace('_caps_udla','').replace('_',' ').capitalize()
            for f in DerivacionCapsUdla._meta.fields
            if f.name not in ('id','ficha')
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_caps_udla': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_caps_udla':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_caps_udla':    forms.DateInput(attrs={'type':'date'}),
        }


class DerivacionOlnForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionOln
        fields = [f.name for f in DerivacionOln._meta.fields if f.name not in ('id','ficha')]
        labels = {
            f.name: f.name.replace('_oln','').replace('_',' ').capitalize()
            for f in DerivacionOln._meta.fields
            if f.name not in ('id','ficha')
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_oln': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_oln':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_oln':    forms.DateInput(attrs={'type':'date'}),
        }

class DerivacionOtroForm(DerivacionBaseForm):
    class Meta(DerivacionBaseForm.Meta):
        model = DerivacionOtro
        fields = [f.name for f in DerivacionOtro._meta.fields if f.name not in ('id','ficha')]
        labels = {
            'institucion_otro': 'Institución (Otro)',
            'descripcion_otro': 'Descripción',
            'fecha_derivacion_otro': 'Fecha de derivación',
            'es_vinculacion_otro': 'Es vinculación',
            'fecha_respuesta_otro': 'Fecha de respuesta',
            'ingresa_otro': 'Ingresa al programa',
            'fecha_ingreso_otro': 'Fecha de ingreso',
        }
        widgets = {
            **DerivacionBaseForm.Meta.widgets,
            'fecha_derivacion_otro': forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta_otro':  forms.DateInput(attrs={'type':'date'}),
            'fecha_ingreso_otro':    forms.DateInput(attrs={'type':'date'}),
        }

from django import forms

TIPOS_DERIVACION = [
    ('', '---------'),
    ('CAVD', 'CAVD'),
    ('URAVIT', 'URAVIT'),
    ('CDM-CAI', 'CDM-CAI'),
    ('SALUD', 'SALUD'),
    ('OFAM', 'OFAM'),
    ('DIDECO', 'DIDECO'),
    ('GESTIÓN TERRITORIAL', 'GESTIÓN TERRITORIAL'),
    ('CAPS UDLA', 'CAPS UDLA'),
    ('OLN', 'OLN'),
    ('OTRO', 'OTRO'),
]


class BuscarDerivacionForm(forms.Form):
    rut = forms.CharField(label='RUT', required=False)
    nombre = forms.CharField(label='Nombre', required=False)
    tipo_derivacion = forms.ChoiceField(label="Tipo de Derivación", choices=TIPOS_DERIVACION, required=False)
    fecha_inicio = forms.DateField(label='Desde', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(label='Hasta', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    solo_con_respuesta = forms.BooleanField(label='Sólo con respuesta', required=False)
    solo_con_ingreso = forms.BooleanField(label='Sólo con ingreso', required=False)
    solo_con_derivacion = forms.BooleanField(label="Solo con fecha de derivación", required=False)
    solo_con_recepcion = forms.BooleanField(label="Solo con fecha de recepción", required=False)
    solo_con_respuesta = forms.BooleanField(label="Solo con fecha de respuesta", required=False)
