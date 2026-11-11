from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import AlumnoForm, MateriaForm
from .models import Alumno, Materia, Patos


class CatalogoTestCase(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='pruebas',
            password='Pruebas#2026',
        )
        self.client.force_login(usuario)
        self.carrera = Patos.objects.create(clave='000001', carrera='TID')

    def test_materia_se_asocia_a_una_carrera(self):
        materia = Materia.objects.create(
            clave='MAT00001',
            nombre='Programación',
            carrera=self.carrera,
        )

        self.assertEqual(materia.carrera, self.carrera)
        self.assertEqual(str(materia), 'MAT00001 - Programación')

    def test_formularios_ofrecen_carreras_como_selector(self):
        self.assertIsInstance(AlumnoForm().fields['carrera'].widget, forms.Select)
        self.assertIsInstance(MateriaForm().fields['carrera'].widget, forms.Select)

    def test_catalogos_y_formularios_se_renderizan(self):
        for route in (
            'lista_carreras',
            'crear_carrera',
            'lista_materias',
            'crear_materia',
        ):
            with self.subTest(route=route):
                self.assertEqual(self.client.get(reverse(route)).status_code, 200)

    def test_detalle_carrera_muestra_registros_relacionados(self):
        alumno = Alumno.objects.create(
            matricula='23TID001',
            nombre='Ana',
            apellido_paterno='Lopez',
            apellido_materno='Garcia',
            edad=20,
            carrera=self.carrera,
        )
        materia = Materia.objects.create(
            clave='MAT00001',
            nombre='Programación',
            carrera=self.carrera,
        )

        response = self.client.get(
            reverse('detalle_carrera', args=[self.carrera.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, alumno.matricula)
        self.assertContains(response, materia.nombre)

    def test_detalle_materia_muestra_carrera(self):
        materia = Materia.objects.create(
            clave='MAT00001',
            nombre='Programación',
            carrera=self.carrera,
        )

        response = self.client.get(
            reverse('detalle_materia', args=[materia.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, materia.nombre)
        self.assertContains(response, self.carrera.carrera)

    def test_formularios_rechazan_envio_vacio(self):
        self.assertEqual(self.client.post(reverse('crear_carrera')).status_code, 200)
        self.assertEqual(self.client.post(reverse('crear_materia')).status_code, 200)

    def test_carrera_no_se_elimina_si_tiene_alumnos(self):
        Alumno.objects.create(
            matricula='23TID001',
            nombre='Ana',
            apellido_paterno='Lopez',
            apellido_materno='Garcia',
            edad=20,
            carrera=self.carrera,
        )

        response = self.client.post(
            reverse('eliminar_carrera', args=[self.carrera.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No se puede eliminar')
        self.assertTrue(Patos.objects.filter(pk=self.carrera.pk).exists())

    def test_carrera_no_se_elimina_si_tiene_materias(self):
        Materia.objects.create(
            clave='MAT00001',
            nombre='Programación',
            carrera=self.carrera,
        )

        response = self.client.post(
            reverse('eliminar_carrera', args=[self.carrera.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No se puede eliminar')
        self.assertTrue(Patos.objects.filter(pk=self.carrera.pk).exists())

    def test_crud_de_carreras(self):
        response = self.client.post(reverse('crear_carrera'), {
            'clave': '000002',
            'carrera': 'Gastronomía',
        })
        self.assertRedirects(response, reverse('lista_carreras'))
        carrera = Patos.objects.get(clave='000002')

        response = self.client.post(
            reverse('editar_carrera', args=[carrera.pk]),
            {'clave': '000002', 'carrera': 'Artes culinarias'},
        )
        self.assertRedirects(response, reverse('lista_carreras'))
        carrera.refresh_from_db()
        self.assertEqual(carrera.carrera, 'Artes culinarias')

        response = self.client.post(reverse('eliminar_carrera', args=[carrera.pk]))
        self.assertRedirects(response, reverse('lista_carreras'))
        self.assertFalse(Patos.objects.filter(pk=carrera.pk).exists())

    def test_crud_de_materias_y_cambio_de_carrera(self):
        otra_carrera = Patos.objects.create(clave='000002', carrera='Arquitectura')
        response = self.client.post(reverse('crear_materia'), {
            'clave': 'MAT00001',
            'nombre': 'Diseño',
            'carrera': self.carrera.pk,
        })
        self.assertRedirects(response, reverse('lista_materias'))
        materia = Materia.objects.get(clave='MAT00001')

        response = self.client.post(
            reverse('editar_materia', args=[materia.pk]),
            {
                'clave': 'MAT00001',
                'nombre': 'Diseño arquitectónico',
                'carrera': otra_carrera.pk,
            },
        )
        self.assertRedirects(response, reverse('lista_materias'))
        materia.refresh_from_db()
        self.assertEqual(materia.nombre, 'Diseño arquitectónico')
        self.assertEqual(materia.carrera, otra_carrera)

        response = self.client.post(reverse('eliminar_materia', args=[materia.pk]))
        self.assertRedirects(response, reverse('lista_materias'))
        self.assertFalse(Materia.objects.filter(pk=materia.pk).exists())
