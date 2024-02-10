from django.urls import path
from .views import *
from .views import inicio, registro, AgregarMaterial, eliminarmaterial, AgregarVehiculo\
,eliminarvehiculo, edicionvehiculo, vervehiculo, ruta, agregarruta, obtener_km, verruta\
, obtener_datos_ruta_material, edicionruta, eliminarruta, rutaconductor, estadorutainiciada\
, estadorutaterminada, reportes,reporterutas,reportematerial,reportevehiculos

urlpatterns = [
    path('', inicio, name="inicio"),
    path('registro/', registro, name="registro"),
    path('Agregar-Material/', AgregarMaterial, name="material"),
    path('Eliminar-Material/<int:id>/', eliminarmaterial, name="eliminarmaterial"),
    path('Editar-Material/<int:id>/', ediciontipoconcepto, name="edicionmaterial"),
    path('Agregar-Vehiculo/', AgregarVehiculo, name="vehiculo"),
    path('Eliminar-Vehiculo/<int:id>/', eliminarvehiculo, name="eliminarvehiculo"),
    path('Editar-Vehiculo/<int:id>/', edicionvehiculo, name="edicionvehiculo"),
    path('Ver-Vehiculo/<int:id>/', vervehiculo, name="vervehiculo"),
    path('Ruta', ruta, name="ruta"),
    path('Ruta/AgregarRuta', agregarruta, name="agregarruta"),
    path('obtener-km/', obtener_km, name='obtener_km'),
    path('obtener-peso-material/', obtener_peso_material, name='obtener_peso_material'),
    path('Ruta/Ver-Ruta/<int:id>/', verruta, name="verruta"),
    path('obtener-datos-ruta-material/', obtener_datos_ruta_material, name='obtener_datos_ruta_material'),
    path('Ruta/Editar-Ruta/<int:id>/', edicionruta, name="edicionruta"),
    path('Ruta/Eliminar-Ruta/<int:id>/', eliminarruta, name="eliminarruta"),
    path('Ruta-Connductor/', rutaconductor, name="rutaconductor"),
    path('Estado-rutainiciada/', estadorutainiciada, name="estadorutainiciada"), 
    path('Estado-rutaterminada/', estadorutaterminada, name="estadorutaterminada"), 
    path('Reportes/', reportes, name="reportes"),      
    path('reporterutas/', reporterutas, name="reporterutas"), 
    path('reportematerial/', reportematerial, name="reportematerial"), 
    path('reportevehiculos/', reportevehiculos, name="reportevehiculos"),                                 
]