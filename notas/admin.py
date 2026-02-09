from django.contrib import admin
from .models import Estudiante, Materia, Nota
from django.db.models import Avg

# 1. Esto permite que las notas aparezcan dentro de la ficha del estudiante
class NotaInline(admin.TabularInline):
    model = Nota
    extra = 1

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # Mostramos las columnas incluyendo las nuevas funciones de cálculo
    list_display = ('nombre', 'apellido', 'municipio', 'colegio', 'get_promedio', 'get_estado')
    list_filter = ('municipio', 'colegio')
    search_fields = ('nombre', 'apellido', 'documento')
    inlines = [NotaInline]

    # Función para calcular el promedio real
    def get_promedio(self, obj):
        # Busca todas las notas de este estudiante y saca el promedio
        promedio = obj.calificaciones.aggregate(Avg('valor'))['valor__avg']
        return round(promedio, 2) if promedio else 0.0
    get_promedio.short_description = 'Promedio'

    # Función para el estado automático
    def get_estado(self, obj):
        promedio = self.get_promedio(obj)
        return "Aprobado" if promedio >= 3.0 else "Reprobado"
    get_estado.short_description = 'Estado'

# Registramos la tabla de Materias por separado
admin.site.register(Materia)