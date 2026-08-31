from django.db import models
from django.contrib.auth.models import User


class Proyecto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, default='')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    propietario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proyectos',
        verbose_name='Propietario'
    )

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre


class Tarea(models.Model):

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título de la tarea')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, default='')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='media',
        verbose_name='Prioridad'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de vencimiento'
    )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='tareas',
        verbose_name='Proyecto'
    )
    asignado_a = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_asignadas',
        verbose_name='Asignado a'
    )

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-prioridad', '-fecha_creacion']

    def __str__(self):
        return f'{self.titulo} - {self.get_estado_display()}'
