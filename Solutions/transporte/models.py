from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Sum, F, Q

class Rol(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre
    
class Tipodocumento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre    

class CustomUser(AbstractUser):
    tipodocumento = models.ForeignKey(Tipodocumento, on_delete=models.SET_NULL, null=True, blank=True)
    documento = models.CharField(max_length=20, default=0)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    licencia = models.CharField(max_length=20, blank=True, null=True)
    SwAtive = models.IntegerField(default=1)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='user permissions',
    )

    def __str__(self):
        return self.first_name + " " + self.last_name

class Material(models.Model):
    nombre = models.CharField(max_length=255)
    presentacion = models.CharField(max_length=255)
    pesounidad = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    def __str__(self):
        return f"{self.nombre} - {self.pesounidad}"  
    
class Ciudad(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    km = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    def __str__(self):
        return self.nombre  

class Vehiculo(models.Model):
    placa = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    year = models.IntegerField(default=0,validators=[MaxValueValidator(limit_value=9999)])
    fechavencisoat = models.DateField()
    fechavencitecno = models.DateField()
    SwAtive = models.IntegerField(default=1)

    def __str__(self):
        return self.placa + " - " + self.marca + " - " + self.modelo    
    
class Ruta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    km = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, null=True)
    estado = models.IntegerField(default=0,validators=[MaxValueValidator(limit_value=1)])
    valortotal = models.DecimalField(default=0.00,decimal_places=2, max_digits=50, null=True)
    SwAtive = models.IntegerField(default=1)
    
   
class Rutamaterial(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    Unidades = models.IntegerField(default=0,validators=[MaxValueValidator(limit_value=9999)])   