from django.contrib import admin
from .models import Estudiante, Materia, Nota
from django.db.models import Avg

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # Esto define las columnas que verás en la tabla de estudiantes
    list_display = ('nombre', 'apellido', 'colegio', 'get_promedio')

    def get_promedio(self, obj):
        # Esta función calcula el promedio real de las notas del alumno
        # Usamos nota_set que es el nombre estándar en Django
        resultado = obj.nota_set.aggregate(Avg('nota'))['nota__avg']
        return round(float(resultado), 2) if resultado else 0.0
    
    get_promedio.short_description = 'Promedio'

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia', 'nota')
    list_filter = ('materia', 'estudiante')
    search_fields = ('estudiante__nombre', 'materia__nombre')
