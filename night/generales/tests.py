from urllib.parse import parse_qs, urlsplit

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AutenticacionTestCase(TestCase):
    def test_inicio_muestra_formulario_de_login(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'auth-entry-horizontal')
        self.assertContains(response, reverse('registro'))

    def test_registro_muestra_animacion_de_escudo(self):
        response = self.client.get(reverse('registro'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'auth-entry-vertical')
        self.assertContains(response, 'auth-entry-door-left')
        self.assertContains(response, 'auth-entry-door-right')
        self.assertContains(response, 'register-shield')
        self.assertContains(response, 'prefers-reduced-motion')
        self.assertContains(response, 'Sincronizando escudo...')

    def test_login_valido_abre_la_lista_de_alumnos(self):
        User.objects.create_user(username='ana', password='Escuela#2026')

        response = self.client.post(reverse('login'), {
            'username': 'ana',
            'password': 'Escuela#2026',
        })

        self.assertRedirects(response, reverse('lista_alumnos'))
        self.assertEqual(
            self.client.get(reverse('lista_alumnos')).status_code,
            200,
        )

    def test_login_invalido_muestra_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'ana',
            'password': 'incorrecta',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos.')

    def test_vistas_escolares_requieren_autenticacion(self):
        rutas = (
            ('lista_alumnos', ()),
            ('detalle_alumno', (1,)),
            ('crear_alumno', ()),
            ('editar_alumno', (1,)),
            ('eliminar_alumno', (1,)),
            ('lista_carreras', ()),
            ('detalle_carrera', (1,)),
            ('crear_carrera', ()),
            ('editar_carrera', (1,)),
            ('eliminar_carrera', (1,)),
            ('lista_materias', ()),
            ('detalle_materia', (1,)),
            ('crear_materia', ()),
            ('editar_materia', (1,)),
            ('eliminar_materia', (1,)),
        )

        for nombre, argumentos in rutas:
            with self.subTest(ruta=nombre):
                destino = reverse(nombre, args=argumentos)
                response = self.client.get(destino)

                self.assertEqual(response.status_code, 302)
                self.assertEqual(urlsplit(response.url).path, reverse('login'))
                self.assertEqual(
                    parse_qs(urlsplit(response.url).query).get('next'),
                    [destino],
                )

    def test_registro_inicia_sesion_y_permite_cerrar_sesion(self):
        response = self.client.post(reverse('registro'), {
            'username': 'nueva',
            'email': 'nueva@example.com',
            'password1': 'Escuela#2026Segura',
            'password2': 'Escuela#2026Segura',
        })

        self.assertRedirects(response, reverse('lista_alumnos'))
        self.assertTrue(
            User.objects.filter(username='nueva').exists(),
        )
        self.assertTrue(
            self.client.get(reverse('lista_alumnos')).wsgi_request.user.is_authenticated,
        )

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
