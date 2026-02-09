import pandas as pd

from django.core.management.base import BaseCommand
from notas.models import Estudiante


class Command(BaseCommand):
    help = "Importa estudiantes desde Excel"

    def handle(self, *args, **kwargs):

        archivo = "estudiantes_final.xlsx"

        try:
            df = pd.read_excel(archivo)
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error leyendo el archivo: {e}"
            ))
            return

        creados = 0
        repetidos = 0

        for index, fila in df.iterrows():

            correo = str(fila.get("correo")).strip()

            if not correo or correo == "nan":
                continue

            existe = Estudiante.objects.filter(email=correo).exists()

            if existe:
                repetidos += 1
                continue

            Estudiante.objects.create(
                nombre=str(fila.get("nombre")).strip(),
                apellido=str(fila.get("apellido")).strip(),
                email=correo,
                documento=str(fila.get("id_estudiante")).strip(),
            )

            creados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Importación terminada. Nuevos: {creados}, Repetidos: {repetidos}"
        ))
