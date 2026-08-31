from django.contrib import admin
from .models import Proyecto, Tarea


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'propietario', 'fecha_creacion']
    list_filter = ['fecha_creacion', 'propietario']
    search_fields = ['nombre', 'descripcion']
    date_hierarchy = 'fecha_creacion'


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'estado', 'prioridad', 'fecha_vencimiento']
    list_filter = ['estado', 'prioridad', 'proyecto']
    search_fields = ['titulo', 'descripcion']
    date_hierarchy = 'fecha_creacion'
