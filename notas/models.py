from django.db import models


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=50)
    email = models.EmailField()

    municipio = models.CharField(max_length=100)
    colegio = models.CharField(max_length=150)


    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    creditos = models.IntegerField()

    def __str__(self):
        return self.nombre


class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    periodo = models.CharField(max_length=20)

def calcular_promedio_estudiante(estudiante):
    notas = Nota.objects.filter(estudiante=estudiante)

    suma = 0
    total = notas.count()

    for n in notas:
        suma += float(n.nota)

    if total > 0:
        promedio = suma / total
    else:
        promedio = 0

    if promedio >= 70:
        estado = "Aprobado"
    else:
        estado = "Reprobado"

    return promedio, estado

class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='calificaciones')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    valor = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.materia.nombre}: {self.valor}"

