# Gestor de Proyectos

Aplicación web en Django para gestionar proyectos y tareas. Proyecto del Módulo 6 - ABP.

## Descripción

La aplicación permite:
- Registrarse e iniciar sesión
- Crear, editar y eliminar proyectos
- Crear, editar y eliminar tareas dentro de cada proyecto
- Ver estadísticas en el dashboard
- Gestionar datos desde el panel de administración

## Tecnologías

- Python 3.12+
- Django 6.1
- SQLite
- Bootstrap 5.3
- HTML5 / CSS3 / JavaScript

## Estructura del proyecto

```
gestor_proyectos/
├── gestor_proyectos/        # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tareas/                  # Aplicación principal
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
├── templates/
│   ├── base.html
│   └── tareas/
│       ├── login.html
│       ├── registro.html
│       ├── home.html
│       ├── perfil.html
│       ├── proyecto_list.html
│       ├── proyecto_detail.html
│       ├── proyecto_form.html
│       ├── proyecto_confirm_delete.html
│       ├── tarea_form.html
│       └── tarea_confirm_delete.html
├── static/
├── manage.py
└── README.md
```

## Instalación

### Requisitos

- Python 3.12 o superior
- pip
- Git (opcional)

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd gestor_proyectos
```

2. Crear entorno virtual:
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

3. Instalar Django:
```bash
pip install django
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario para el admin:
```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor:
```bash
python manage.py runserver
```

7. Abrir en el navegador:
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Funcionalidades

- Registro de usuarios con validaciones
- Login/logout con django.contrib.auth
- CRUD completo de proyectos y tareas
- Herencia de plantillas (base.html)
- Formularios con validaciones
- Diseño responsivo con Bootstrap 5
- Panel admin personalizado
- Protección CSRF
- Vistas protegidas con LoginRequiredMixin
- Cada usuario solo ve sus propios proyectos

## Pruebas

Ejecutar las pruebas:
```bash
python manage.py test
```

Con más detalle:
```bash
python manage.py test --verbosity=2
```

## Autor

Proyecto del Módulo 6 - ABP.