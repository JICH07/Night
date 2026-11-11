from django import forms

from .models import Alumno, Materia, Patos

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'edad', 'carrera']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'hud-input', 'placeholder': 'Ej. 23TID021'}),
            'nombre': forms.TextInput(attrs={'class': 'hud-input', 'placeholder': 'Nombre(s)'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'hud-input', 'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'hud-input', 'placeholder': 'Apellido Materno'}),
            'edad': forms.NumberInput(attrs={'class': 'hud-input'}),
            'carrera': forms.Select(attrs={'class': 'hud-input'}),
        }


class CarreraForm(forms.ModelForm):
    class Meta:
        model = Patos
        fields = ['clave', 'carrera']
        widgets = {
            'clave': forms.TextInput(attrs={
                'class': 'hud-input',
                'placeholder': 'Ej. 000004',
            }),
            'carrera': forms.TextInput(attrs={
                'class': 'hud-input',
                'placeholder': 'Nombre de la carrera',
            }),
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['clave', 'nombre', 'carrera']
        widgets = {
            'clave': forms.TextInput(attrs={
                'class': 'hud-input',
                'placeholder': 'Clave de la materia',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'hud-input',
                'placeholder': 'Nombre de la materia',
            }),
            'carrera': forms.Select(attrs={'class': 'hud-input'}),
        }