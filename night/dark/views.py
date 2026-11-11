from django.contrib.auth.decorators import login_required
from django.db.models import Count, ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlumnoForm, CarreraForm, MateriaForm
from .models import Alumno, Materia, Patos


@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'lista_alumnos.html', {'alumnos': alumnos})


@login_required
def detalle_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    return render(request, 'detalle_alumno.html', {'alumno': alumno})


@login_required
def crear_alumno(request):
    if request.method == 'POST':
        formulario = AlumnoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_alumnos')
    else:
        formulario = AlumnoForm()
    
    return render(request, 'crear_alumno.html', {'formulario': formulario, 'accion': 'Registrar'})


@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        formulario = AlumnoForm(request.POST, instance=alumno)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_alumnos')
    else:
        formulario = AlumnoForm(instance=alumno)
        
    return render(request, 'crear_alumno.html', {'formulario': formulario, 'accion': 'Modificar'})


@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')
    return render(request, 'confirmar_eliminar.html', {'alumno': alumno})


@login_required
def lista_carreras(request):
    carreras = Patos.objects.annotate(
        alumnos_count=Count('alumno', distinct=True),
        materias_count=Count('materia', distinct=True),
    ).order_by('clave')
    return render(request, 'lista_carreras.html', {'carreras': carreras})


@login_required
def detalle_carrera(request, pk):
    carrera = get_object_or_404(
        Patos.objects.prefetch_related('alumno_set', 'materia_set'),
        pk=pk,
    )
    return render(request, 'detalle_carrera.html', {'carrera': carrera})


@login_required
def crear_carrera(request):
    formulario = CarreraForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('lista_carreras')
    return render(request, 'catalogo_form.html', {
        'formulario': formulario,
        'accion': 'Registrar',
        'tipo': 'Carrera',
        'lista_url': 'lista_carreras',
    })


@login_required
def editar_carrera(request, pk):
    carrera = get_object_or_404(Patos, pk=pk)
    formulario = CarreraForm(
        request.POST if request.method == 'POST' else None,
        instance=carrera,
    )
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('lista_carreras')
    return render(request, 'catalogo_form.html', {
        'formulario': formulario,
        'accion': 'Modificar',
        'tipo': 'Carrera',
        'lista_url': 'lista_carreras',
    })


@login_required
def eliminar_carrera(request, pk):
    carrera = get_object_or_404(Patos, pk=pk)
    contexto = {
        'objeto': carrera,
        'tipo': 'Carrera',
        'lista_url': 'lista_carreras',
        'alumnos_count': carrera.alumno_set.count(),
        'materias_count': carrera.materia_set.count(),
    }
    if request.method == 'POST':
        try:
            carrera.delete()
        except ProtectedError:
            contexto['error'] = (
                'No se puede eliminar esta carrera mientras tenga alumnos o '
                'materias asociados.'
            )
        else:
            return redirect('lista_carreras')
    return render(request, 'confirmar_eliminacion_catalogo.html', contexto)


@login_required
def lista_materias(request):
    materias = Materia.objects.select_related('carrera').all()
    return render(request, 'lista_materias.html', {'materias': materias})


@login_required
def detalle_materia(request, pk):
    materia = get_object_or_404(
        Materia.objects.select_related('carrera'),
        pk=pk,
    )
    return render(request, 'detalle_materia.html', {'materia': materia})


@login_required
def crear_materia(request):
    formulario = MateriaForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('lista_materias')
    return render(request, 'catalogo_form.html', {
        'formulario': formulario,
        'accion': 'Registrar',
        'tipo': 'Materia',
        'lista_url': 'lista_materias',
    })


@login_required
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    formulario = MateriaForm(
        request.POST if request.method == 'POST' else None,
        instance=materia,
    )
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('lista_materias')
    return render(request, 'catalogo_form.html', {
        'formulario': formulario,
        'accion': 'Modificar',
        'tipo': 'Materia',
        'lista_url': 'lista_materias',
    })


@login_required
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        materia.delete()
        return redirect('lista_materias')
    return render(request, 'confirmar_eliminacion_catalogo.html', {
        'objeto': materia,
        'tipo': 'Materia',
        'lista_url': 'lista_materias',
    })