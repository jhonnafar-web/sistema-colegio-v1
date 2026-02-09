from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os

# --- MODELOS ---
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

# --- FUNCIÓN PARA GOOGLE SHEETS (REPARTE EN COLUMNAS) ---
def enviar_a_google(datos_lista):
    try:
        path_to_json = os.path.join(os.getcwd(), 'google-credentials.json')
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scope)
        client = gspread.authorize(creds)
        sheet = client.open("respaldo").sheet1
        
        # La fila tendrá: [FECHA, USUARIO, ESTUDIANTE, MATERIA, NOTA]
        fila = [datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")] + datos_lista
        
        sheet.append_row(fila)
        print(f"✅ Sincronizado en columnas: {datos_lista}")
    except Exception as e:
        print(f"❌ Error en Google Sheets: {e}")

# --- SEÑALES PARA REACCIONAR A CAMBIOS ---

@receiver(post_save, sender=Nota)
def señal_nota(sender, instance, **kwargs):
    # Organiza la información en 4 columnas después de la fecha
    datos = [
        "Admin-Render", 
        str(instance.estudiante), 
        str(instance.materia), 
        float(instance.nota)
    ]
    enviar_a_google(datos)

@receiver(post_save, sender=Estudiante)
def señal_estudiante(sender, instance, **kwargs):
    # Organiza la información para cuando se edita un alumno
    datos = [
        "Admin-Render", 
        f"{instance.nombre} {instance.apellido}", 
        "ACTUALIZACIÓN PERFIL", 
        "-"
    ]
    enviar_a_google(datos)
