from django.contrib import admin
from .models import Rol, CustomUser, Tipodocumento, Material, Ciudad, Vehiculo, Ruta, Rutamaterial

admin.site.register(Rol)
admin.site.register(CustomUser)
admin.site.register(Tipodocumento)
admin.site.register(Material)
admin.site.register(Ciudad)
admin.site.register(Vehiculo)
admin.site.register(Ruta)
admin.site.register(Rutamaterial)
