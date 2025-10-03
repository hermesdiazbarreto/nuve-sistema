from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]
    
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    cedula_nit = models.CharField(max_length=20, unique=True)
    tipo_cliente = models.CharField(max_length=10, choices=TIPO_CHOICES, default='natural')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}".strip()
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_registro']