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

class FichaAcogidaForm(forms.ModelForm):
    class Meta:
        model = FichaAcogida
        exclude = ['profesional']
        fields = '__all__'
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_contacto_1': forms.DateInput(attrs={'type': 'date'}),
            'fecha_contacto_2': forms.DateInput(attrs={'type': 'date'}),
            'fecha_contacto_3': forms.DateInput(attrs={'type': 'date'}),

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

class PersonaAtendidaForm(forms.ModelForm):
    class Meta:
        model = PersonaAtendida
        exclude = ['ficha', 'edad', 'rango_etareo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()}),
        }
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = [  # define TODO excepto 'ficha'
            'tiene_denuncia', 'anio_denuncia', 'lugar_denuncia', 'numero_causa',
            'medida_cautelar', 'dificultades_denuncia',
            'descripcion_dificultad', 'motivo_denuncia'
        ]


class MotivoIngresoForm(forms.ModelForm):
    class Meta:
        model = MotivoIngreso
        fields = '__all__'
        exclude = ['ficha']  # ✅ esto es clave

from django import forms
from fichas.models import AspectosPsicologicos

ACTITUD_CHOICES = [
    ('colaboradora', 'Colaboradora'),
    ('reticente', 'Reticente'),
    ('querellante', 'Querellante'),
    ('agresiva', 'Agresiva'),
    ('inhibida', 'Inhibida'),
]

LENGUAJE_CHOICES = [
    ('verborreico', 'Verborreico'),
    ('mutismo', 'Mutismo'),
    ('neologismos', 'Neologismos'),
]

AFECTIVIDAD_CHOICES = [
    ('humor_expansivo', 'Humor expansivo'),
    ('humor_deprimido', 'Humor deprimido'),
    ('indiferencia_afectiva', 'Indiferencia afectiva'),
    ('labilidad', 'Labilidad'),
]

SUENO_CHOICES = [
    ('insomnio', 'Insomnio'),
    ('hipersomnia', 'Hipersomnia'),
]

ALIMENTACION_CHOICES = [
    ('anorexia', 'Anorexia'),
    ('negativa_a_comer', 'Negativa a comer'),
    ('hiporexia', 'Hiporexia'),
]

LIMITACION_CHOICES = [
    ('no_puede_salir', 'No puede salir'),
    ('no_puede_realizar_actividades', 'No puede realizar actividades habituales'),
]

ESTADO_CONCIENCIA_CHOICES = [
    ('lucido', 'Lúcido'),
    ('obnubilado', 'Obnubilado'),
]

ORIENTACION_CHOICES = [
    ('desorientacion_temporal', 'Desorientación temporal'),
    ('desorientacion_espacial', 'Desorientación espacial'),
]

ESTADO_COGNITIVO_CHOICES = [
    ('atencion', 'Problemas de atención'),
    ('concentracion', 'Problemas de concentración'),
    ('memoria', 'Problemas de memoria'),
]





class AspectosPsicologicosForm(forms.ModelForm):
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

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Campos multiseleccionables
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
            'objetivos': forms.TextInput(attrs={'placeholder': 'Objetivo/s...'}),
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
            'uav_psicologica_1_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_psicologica_2_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_psicologica_3_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_social_1_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_social_2_detalle': forms.Textarea(attrs={'rows': 2}),
            'uav_social_3_detalle': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
