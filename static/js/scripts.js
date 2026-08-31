// scripts.js - Gestor de Proyectos

document.addEventListener('DOMContentLoaded', function() {

    // cerrar alertas despues de 5 segundos
    var alertas = document.querySelectorAll('.alert');
    alertas.forEach(function(alerta) {
        setTimeout(function() {
            var botonCerrar = alerta.querySelector('.btn-close');
            if (botonCerrar) {
                botonCerrar.click();
            }
        }, 5000);
    });

    // confirmacion antes de eliminar
    var botonesEliminar = document.querySelectorAll('[data-confirm-eliminar]');
    botonesEliminar.forEach(function(boton) {
        boton.addEventListener('click', function(e) {
            var mensaje = boton.getAttribute('data-confirm-eliminar');
            if (!confirm(mensaje)) {
                e.preventDefault();
            }
        });
    });

    // color del badge segun estado
    var badgesEstado = document.querySelectorAll('.badge-estado');
    badgesEstado.forEach(function(badge) {
        var estado = badge.textContent.trim().toLowerCase();
        if (estado === 'pendiente') {
            badge.classList.add('bg-warning', 'text-dark');
        } else if (estado === 'en progreso') {
            badge.classList.add('bg-primary', 'text-white');
        } else if (estado === 'completada') {
            badge.classList.add('bg-success', 'text-white');
        }
    });

    // color del badge segun prioridad
    var badgesPrioridad = document.querySelectorAll('.badge-prioridad');
    badgesPrioridad.forEach(function(badge) {
        var prioridad = badge.textContent.trim().toLowerCase();
        if (prioridad === 'alta') {
            badge.classList.add('bg-danger', 'text-white');
        } else if (prioridad === 'media') {
            badge.classList.add('bg-warning', 'text-dark');
        } else if (prioridad === 'baja') {
            badge.classList.add('bg-info', 'text-dark');
        }
    });

    // tooltips de bootstrap
    var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

});