import re
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Usuario, NivelEducativo, Area, Asignatura, Grado, Grupo, PlanDeLeccion, Tema, Aula, AsignarDocente


#Formulario para registro y logueo de usuarios
class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget= forms.PasswordInput(attrs={
            'class': 'form-control bg-light-subtle border-0 shadow-sm', 
            'placeholder': 'contraseña'
        }),
        help_text= 'Debe tener al menos 8 caracteres, una mayuscula, una minuscula, un digito y un caracter especial (!$%&/?¡_-)'
    )
    
    confirmar_password = forms.CharField(
        widget= forms.PasswordInput(attrs={
            'class':' form-control bg-light-subtle border-0 shadow-sm',
            'placeholder': 'Confirmar contraseña'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ['tipo_documento', 'numero_documento', 'rol', 'email', 'password']
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'numero_documento': forms.NumberInput(attrs={
                'class': 'form-control bg-light-subtle border-0 shadow-sm',
                'placeholder': 'Numero de documento'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light-subtle border-0 shadow-sm',
                'placeholder': 'Correo electronico'
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if password != confirmar_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener almenos 8 carácteres.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('La contraseña debe tener almenos una mayuscula.')
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('La contraseña debe tener almenos una minuscula.')
        if not re.search(r'\d', password):
            raise forms.ValidationError('La contraseña debe tener almenos un digito.')
        if not re.search(r'[!\$%&/?¡_-]', password):
            raise forms.ValidationError('La Contraseña debe tener almenos un caracter especial')
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.is_active = False
        if commit:
            usuario.save()
        return usuario

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electronico'
        })
    )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label= 'Contraseña'
    )

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

class AsignacionDocenteForm(forms.ModelForm):
    class Meta:
        model = AsignarDocente
        fields = ['docente', 'asignatura', 'aula']
        widgets = {
            'docente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'asignatura': forms.Select(attrs={
                'class': 'form-select'
            }),
            'aula': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class EstadoDocenteForm(forms.ModelForm): #DEFECTUOSO
    class Meta:
        model =Usuario
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch',
                'id': 'switchDocente'
            }),
        }
