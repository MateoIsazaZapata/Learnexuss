import re
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import NivelEducativo, Area, Asignatura, Grado, Grupo, PlanDeLeccion, Tema, Aula

#Formulario crear aulas
class aulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['grado', 'grupo', 'asignaturas']
        widgets = {
            'grado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'grupo': forms.Select(attrs={
                'class': 'forms-select'
            }),
            'asignaturas': forms.CheckboxSelectMultiple(attrs={
                'class': 'forms-select'
            })
        }


#Formularios Nivel educativo
class NivelEducativoForm(forms.ModelForm):
    class Meta:
        model = NivelEducativo
        fields = ['nivel']


class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ['grado', 'nivel_educativo']
        widgets = {
            'grado': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 shadow-sm',
                'placeholder': 'Nombre del grado',
            }),
            'nivel_educativo': forms.Select(attrs={
                'class': 'form-select',
            })
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['grupo', 'grado_asignado']
        widgets = {
            'grupo': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 shadow-sm',
                'placeholder': 'Nombre del Grupo'
            }),
            'grado_asignado': forms.Select(attrs={
                'class': 'form-select',
            })
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['area']
        widgets = {
            'area': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 shadow-sm',
                'placeholder': 'Nombre del area'
            })
        }

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['asignatura', 'area_asignada', 'grado_asignado']
        widgets = {
            'asignatura': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 shadow-sm',
                'placeholder': 'Nombre de asignatura',
            }),
            'area_asignada': forms.Select(attrs={
                'class': 'form-select'
            }),
            'grado_asignado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class TemasForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['tema', 'asignatura_asignada']
        widgets = {
            'tema': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 shadow-sm',
                'placeholder': 'Nombre del tema'
            }),
            'asignatura_asignada': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class PlanDeLeccionForm(forms.ModelForm):
    class Meta:
        model = PlanDeLeccion
        fields = ['plan_leccion', 'area', 'tema', 'archivo_plan']
        widgets = {
            'plan_leccion': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 shadow-sm',
                'placeholder': 'Nombre de plan de lección'
            }),
            'area': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tema': forms.Select(attrs={
                'class': 'form-select'
            }),
            'archivo_plan': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }