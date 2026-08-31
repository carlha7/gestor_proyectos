from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tareas'

urlpatterns = [
    # ---- Autenticación ----
    path('login/', auth_views.LoginView.as_view(template_name='tareas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # ---- Home / Dashboard ----
    path('', views.HomeView.as_view(), name='home'),

    # ---- Proyectos ----
    path('proyectos/', views.ProyectoListView.as_view(), name='proyecto_list'),
    path('proyecto/crear/', views.ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyecto/<int:pk>/', views.ProyectoDetailView.as_view(), name='proyecto_detail'),
    path('proyecto/<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyecto/<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='proyecto_delete'),

    # ---- Tareas ----
    path('proyecto/<int:proyecto_pk>/tarea/crear/', views.tarea_create_view, name='tarea_create'),
    path('tarea/<int:pk>/editar/', views.tarea_update_view, name='tarea_update'),
    path('tarea/<int:pk>/eliminar/', views.tarea_delete_view, name='tarea_delete'),

    # ---- Perfil ----
    path('perfil/', views.perfil_view, name='perfil'),
]
