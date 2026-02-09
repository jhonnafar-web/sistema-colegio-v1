from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os

# --- 1. MODELOS ---

class Estudiante(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200, default=" ", blank=True)
    municipio = models.CharField(max_length=200, default=" ", blank=True)
    colegio = models.CharField(max_length=200, default=" ", blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2, default=0.0) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.estudiante} - {self.materia}: {self.nota}"

# --- 2. FUNCIÓN DE ENVÍO A GOOGLE SHEETS ---

def enviar_datos_a_google(mensaje_log):
    try:
        # En Render, os.getcwd() es la carpeta raíz donde está el json
        path_to_json = os.path.join(os.getcwd(), 'google-credentials.json')

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scope)
        client = gspread.authorize(creds)
        
        # Debe existir un archivo en Google Drive llamado "respaldo"
        sheet = client.open("respaldo").sheet1

        fila = [
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Admin-Render",
            mensaje_log
        ]
        
        sheet.append_row(fila)
        print(f"✅ ÉXITO: {mensaje_log}")
    except Exception as e:
        print(f"❌ ERROR EN EL RESPALDO: {e}")

# --- 3. DISPARADORES (SIGNALS) ---

@receiver(post_save, sender=Nota)
def señal_nota(sender, instance, **kwargs):
    # Esto se activa al guardar una nota
    texto = f"Nota Guardada: {instance.estudiante} | Materia: {instance.materia} | Valor: {instance.nota}"
    enviar_datos_a_google(texto)

@receiver(post_save, sender=Estudiante)
def señal_estudiante(sender, instance, **kwargs):
    # Esto se activa al editar o crear un estudiante
    texto = f"Cambio en Estudiante: {instance.nombre} {instance.apellido} | Colegio: {instance.colegio}"
    enviar_datos_a_google(texto)
