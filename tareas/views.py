from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Proyecto, Tarea
from .forms import RegistroForm, ProyectoForm, TareaForm


# Autenticación

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido/a {user.first_name}.')
            return redirect('tareas:login')
    else:
        form = RegistroForm()
    return render(request, 'tareas/registro.html', {'form': form})


# Home / Dashboard

class HomeView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'tareas/home.html'
    context_object_name = 'proyectos'

    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_proyectos'] = self.get_queryset().count()
        context['tareas_pendientes'] = Tarea.objects.filter(
            proyecto__propietario=self.request.user,
            estado='pendiente'
        ).count()
        context['tareas_en_progreso'] = Tarea.objects.filter(
            proyecto__propietario=self.request.user,
            estado='en_progreso'
        ).count()
        context['tareas_completadas'] = Tarea.objects.filter(
            proyecto__propietario=self.request.user,
            estado='completada'
        ).count()
        return context


# Proyectos (CRUD)

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'tareas/proyecto_list.html'
    context_object_name = 'proyectos'

    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'tareas/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = self.object.tareas.all()
        context['form_tarea'] = TareaForm(proyecto=self.object)
        return context


class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'tareas/proyecto_form.html'

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        messages.success(self.request, '¡Proyecto creado exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tareas:proyecto_detail', kwargs={'pk': self.object.pk})


class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'tareas/proyecto_form.html'

    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '¡Proyecto actualizado exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tareas:proyecto_detail', kwargs={'pk': self.object.pk})


class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'tareas/proyecto_confirm_delete.html'
    success_url = reverse_lazy('tareas:proyecto_list')

    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, '¡Proyecto eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)


# Tareas (CRUD)

@login_required
def tarea_create_view(request, proyecto_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk, propietario=request.user)

    if request.method == 'POST':
        form = TareaForm(request.POST, proyecto=proyecto)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            messages.success(request, '¡Tarea creada exitosamente!')
            return redirect('tareas:proyecto_detail', pk=proyecto.pk)
    else:
        form = TareaForm(proyecto=proyecto)

    return render(request, 'tareas/tarea_form.html', {
        'form': form,
        'proyecto': proyecto
    })


@login_required
def tarea_update_view(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__propietario=request.user)

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea, proyecto=tarea.proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tarea actualizada exitosamente!')
            return redirect('tareas:proyecto_detail', pk=tarea.proyecto.pk)
    else:
        form = TareaForm(instance=tarea, proyecto=tarea.proyecto)

    return render(request, 'tareas/tarea_form.html', {
        'form': form,
        'proyecto': tarea.proyecto,
        'tarea': tarea
    })


@login_required
def tarea_delete_view(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__propietario=request.user)
    proyecto_pk = tarea.proyecto.pk

    if request.method == 'POST':
        tarea.delete()
        messages.success(request, '¡Tarea eliminada exitosamente!')
        return redirect('tareas:proyecto_detail', pk=proyecto_pk)

    return render(request, 'tareas/tarea_confirm_delete.html', {'tarea': tarea})


# Perfil

@login_required
def perfil_view(request):
    proyectos = Proyecto.objects.filter(propietario=request.user)
    tareas = Tarea.objects.filter(proyecto__propietario=request.user)

    context = {
        'proyectos_count': proyectos.count(),
        'tareas_count': tareas.count(),
        'tareas_pendientes': tareas.filter(estado='pendiente').count(),
        'tareas_completadas': tareas.filter(estado='completada').count(),
    }
    return render(request, 'tareas/perfil.html', context)
