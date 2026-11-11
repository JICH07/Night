from django.db import models


class Alumno(models.Model):
    matricula = models.CharField(verbose_name='Matricula', max_length=8, unique=True)
    nombre = models.CharField(verbose_name='Nombre alumno', max_length=50)
    apellido_paterno = models.CharField(verbose_name='Apellido paterno', max_length=100)
    apellido_materno = models.CharField(verbose_name='Apellido materno', max_length=100)
    edad = models.IntegerField(verbose_name='Edad')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    carrera = models.ForeignKey('Patos', on_delete=models.PROTECT, verbose_name='Carrera')

    def __str__(self):
        return f'{self.matricula} - {self.nombre}'


class Patos(models.Model):
    clave = models.CharField(verbose_name='Clave', max_length=8, unique=True)
    carrera = models.CharField(verbose_name='Nombre Carrera', max_length=50)

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

    def __str__(self):
        return f'{self.clave} - {self.carrera}'


class Materia(models.Model):
    clave = models.CharField(verbose_name='Clave', max_length=8, unique=True)
    nombre = models.CharField(verbose_name='Nombre de la materia', max_length=100)
    carrera = models.ForeignKey(
        Patos,
        on_delete=models.PROTECT,
        verbose_name='Carrera',
    )

    class Meta:
        ordering = ['carrera__clave', 'clave']
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'

    def __str__(self):
        return f'{self.clave} - {self.nombre}'