from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alumno/<int:pk>/', views.detalle_alumno, name='detalle_alumno'),
    path('alumno/nuevo/', views.crear_alumno, name='crear_alumno'),
    path('alumno/editar/<int:pk>/', views.editar_alumno, name='editar_alumno'),
    path('alumno/eliminar/<int:pk>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('carrera/<int:pk>/', views.detalle_carrera, name='detalle_carrera'),
    path('carrera/nueva/', views.crear_carrera, name='crear_carrera'),
    path('carrera/editar/<int:pk>/', views.editar_carrera, name='editar_carrera'),
    path('carrera/eliminar/<int:pk>/', views.eliminar_carrera, name='eliminar_carrera'),
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materia/<int:pk>/', views.detalle_materia, name='detalle_materia'),
    path('materia/nueva/', views.crear_materia, name='crear_materia'),
    path('materia/editar/<int:pk>/', views.editar_materia, name='editar_materia'),
    path('materia/eliminar/<int:pk>/', views.eliminar_materia, name='eliminar_materia'),
]