from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta

from .models import Proyecto, Tarea
from .forms import RegistroForm, ProyectoForm, TareaForm


class ProyectoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_crear_proyecto(self):
        proyecto = Proyecto.objects.create(
            nombre='Proyecto de prueba',
            descripcion='Una descripción de prueba',
            propietario=self.user
        )
        self.assertEqual(proyecto.nombre, 'Proyecto de prueba')
        self.assertEqual(proyecto.propietario, self.user)

    def test_str_proyecto(self):
        proyecto = Proyecto.objects.create(
            nombre='Mi Proyecto',
            propietario=self.user
        )
        self.assertEqual(str(proyecto), 'Mi Proyecto')

    def test_orden_proyectos(self):
        p1 = Proyecto.objects.create(nombre='Primero', propietario=self.user)
        p2 = Proyecto.objects.create(nombre='Segundo', propietario=self.user)
        proyectos = list(Proyecto.objects.all())
        self.assertEqual(proyectos[0], p2)


class TareaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto test',
            propietario=self.user
        )

    def test_crear_tarea(self):
        tarea = Tarea.objects.create(
            titulo='Tarea de prueba',
            proyecto=self.proyecto
        )
        self.assertEqual(tarea.titulo, 'Tarea de prueba')
        self.assertEqual(tarea.estado, 'pendiente')

    def test_str_tarea(self):
        tarea = Tarea.objects.create(
            titulo='Hacer algo',
            proyecto=self.proyecto
        )
        self.assertEqual(str(tarea), 'Hacer algo - Pendiente')

    def test_estado_default(self):
        tarea = Tarea.objects.create(
            titulo='Nueva tarea',
            proyecto=self.proyecto
        )
        self.assertEqual(tarea.estado, 'pendiente')
        self.assertEqual(tarea.prioridad, 'media')

    def test_cambiar_estado(self):
        tarea = Tarea.objects.create(
            titulo='Tarea estado',
            proyecto=self.proyecto
        )
        tarea.estado = 'completada'
        tarea.save()
        self.assertEqual(tarea.estado, 'completada')


class RegistroFormTest(TestCase):

    def test_form_registro_valido(self):
        form_data = {
            'username': 'nuevouser',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'nuevo@test.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_registro_email_duplicado(self):
        User.objects.create_user(
            username='existente',
            email='ya@existe.com',
            password='pass1234567'
        )
        form_data = {
            'username': 'otrousuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'ya@existe.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_registro_password_distinta(self):
        form_data = {
            'username': 'nuevouser',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'test@test.com',
            'password1': 'TestPass123!',
            'password2': 'OtraPass456!',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProyectoFormTest(TestCase):

    def test_form_proyecto_valido(self):
        form_data = {
            'nombre': 'Mi Proyecto',
            'descripcion': 'Desc',
        }
        form = ProyectoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_proyecto_nombre_corto(self):
        form_data = {
            'nombre': 'AB',
            'descripcion': '',
        }
        form = ProyectoForm(data=form_data)
        self.assertFalse(form.is_valid())


class TareaFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto test',
            propietario=self.user
        )

    def test_form_tarea_valido(self):
        form_data = {
            'titulo': 'Mi tarea',
            'estado': 'pendiente',
            'prioridad': 'media',
        }
        form = TareaForm(data=form_data, proyecto=self.proyecto)
        self.assertTrue(form.is_valid())

    def test_form_tarea_titulo_corto(self):
        form_data = {
            'titulo': 'AB',
            'estado': 'pendiente',
            'prioridad': 'media',
        }
        form = TareaForm(data=form_data, proyecto=self.proyecto)
        self.assertFalse(form.is_valid())

    def test_form_tarea_fecha_pasada(self):
        form_data = {
            'titulo': 'Tarea fecha',
            'estado': 'pendiente',
            'prioridad': 'media',
            'fecha_vencimiento': '2020-01-01',
        }
        form = TareaForm(data=form_data, proyecto=self.proyecto)
        self.assertFalse(form.is_valid())


class AuthViewTest(TestCase):

    def test_registro_get(self):
        response = self.client.get(reverse('tareas:registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tareas/registro.html')

    def test_registro_post_valido(self):
        response = self.client.post(reverse('tareas:registro'), {
            'username': 'nuevouser',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'nuevo@test.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(User.objects.count(), 1)

    def test_registro_post_invalido(self):
        response = self.client.post(reverse('tareas:registro'), {
            'username': '',
            'password1': 'corto',
        })
        self.assertEqual(User.objects.count(), 0)

    def test_login_get(self):
        response = self.client.get(reverse('tareas:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_post_valido(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post(reverse('tareas:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalido(self):
        response = self.client.post(reverse('tareas:login'), {
            'username': 'noexiste',
            'password': 'malapass',
        })
        self.assertEqual(response.status_code, 200)


class ProyectoViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_home(self):
        response = self.client.get(reverse('tareas:home'))
        self.assertEqual(response.status_code, 200)

    def test_proyecto_list(self):
        response = self.client.get(reverse('tareas:proyecto_list'))
        self.assertEqual(response.status_code, 200)

    def test_proyecto_create_get(self):
        response = self.client.get(reverse('tareas:proyecto_create'))
        self.assertEqual(response.status_code, 200)

    def test_proyecto_create_post(self):
        response = self.client.post(reverse('tareas:proyecto_create'), {
            'nombre': 'Proyecto nuevo',
            'descripcion': 'Desc',
        })
        self.assertEqual(Proyecto.objects.count(), 1)

    def test_proyecto_update(self):
        proyecto = Proyecto.objects.create(
            nombre='Proyecto edit',
            propietario=self.user
        )
        response = self.client.post(
            reverse('tareas:proyecto_update', kwargs={'pk': proyecto.pk}),
            {'nombre': 'Editado', 'descripcion': 'Nueva desc'}
        )
        proyecto.refresh_from_db()
        self.assertEqual(proyecto.nombre, 'Editado')

    def test_proyecto_delete(self):
        proyecto = Proyecto.objects.create(
            nombre='Proyecto borrar',
            propietario=self.user
        )
        response = self.client.post(
            reverse('tareas:proyecto_delete', kwargs={'pk': proyecto.pk})
        )
        self.assertEqual(Proyecto.objects.count(), 0)

    def test_proyecto_no_propietario(self):
        otro = User.objects.create_user(username='otro', password='pass1234567')
        proyecto = Proyecto.objects.create(
            nombre='Proyecto otro',
            propietario=otro
        )
        response = self.client.get(
            reverse('tareas:proyecto_detail', kwargs={'pk': proyecto.pk})
        )
        self.assertEqual(response.status_code, 404)


class TareaViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto test',
            propietario=self.user
        )
        self.client.login(username='testuser', password='testpass123')

    def test_tarea_create_get(self):
        response = self.client.get(
            reverse('tareas:tarea_create', kwargs={'proyecto_pk': self.proyecto.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_tarea_create_post(self):
        response = self.client.post(
            reverse('tareas:tarea_create', kwargs={'proyecto_pk': self.proyecto.pk}),
            {'titulo': 'Nueva tarea', 'estado': 'pendiente', 'prioridad': 'media'}
        )
        self.assertEqual(Tarea.objects.count(), 1)

    def test_tarea_update(self):
        tarea = Tarea.objects.create(
            titulo='Tarea editar',
            proyecto=self.proyecto
        )
        response = self.client.post(
            reverse('tareas:tarea_update', kwargs={'pk': tarea.pk}),
            {'titulo': 'Editada', 'estado': 'en_progreso', 'prioridad': 'alta'}
        )
        tarea.refresh_from_db()
        self.assertEqual(tarea.titulo, 'Editada')

    def test_tarea_delete(self):
        tarea = Tarea.objects.create(
            titulo='Tarea borrar',
            proyecto=self.proyecto
        )
        response = self.client.post(
            reverse('tareas:tarea_delete', kwargs={'pk': tarea.pk})
        )
        self.assertEqual(Tarea.objects.count(), 0)
