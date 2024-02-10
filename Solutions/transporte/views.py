from django.shortcuts import render,redirect
from django.views.generic import DetailView, TemplateView, RedirectView, View
from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm, MaterialForm, VehiculoForm, RutaForm, RutaMaterialForm, Rutamaterial
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Q
from django.utils.decorators import method_decorator
# Crear pdf
import os
import re
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .models import Material, Rutamaterial, Vehiculo, Ruta, Ciudad, CustomUser
from datetime import date
from django.http import JsonResponse
from decimal import Decimal, ROUND_HALF_UP
import json
import datetime
from .generator import XlsGenerator
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.styles import Border, PatternFill, Font, Alignment
import xlsxwriter
# Create your views here.


@login_required(login_url='login')
def inicio(request):
    return render(request, 'transporte/inicio.html')

@login_required(login_url='login')
def registro(request):
    data = {'form': CustomUserCreationForm}

    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            rol_value = formulario.cleaned_data['rol']
            if rol_value.id == 2:
                licencia_value = formulario.cleaned_data['licencia']
                if len(licencia_value) > 0:
                    formulario.save()
                    return redirect('inicio')
                else:
                    data['alerta'] = formulario.errors
                    print(formulario.errors)
            else:
                formulario.save()
                return redirect('inicio')
        else:
            data['alerta'] = formulario.errors
            print(formulario.errors)

        data['form'] = formulario        

    return render(request, 'registration/registro.html', data)

# FORMULARIO MATERIAL

@login_required(login_url='login')
def AgregarMaterial(request):
    material = Material.objects.all()
    for m in material:
        m.ruta = 1 if Rutamaterial.objects.filter(material=m.id).exists() else 0

    data = {'form': MaterialForm,
            'material': material}

    if request.method == 'POST':
        formulario = MaterialForm(request.POST)
        if formulario.is_valid():            
                formulario.save()
                return redirect('material')
        else:
            data['alerta'] = formulario.errors
            print(formulario.errors)

        data['form'] = formulario        

    return render(request, 'transporte/material.html', data)

@login_required(login_url='login')
def eliminarmaterial(request, id):
    material = get_object_or_404(Material, id=id)
    material.delete()

    return redirect(AgregarMaterial)

@login_required(login_url='login')
def ediciontipoconcepto(request, id):
    material = get_object_or_404(Material, id=id)
    data = {'form': MaterialForm(instance=material)}

    if request.method == 'POST':
        formulario = MaterialForm(request.POST, instance=material)
        if formulario.is_valid():
            formulario.save()
            return redirect('material')        
    else: 
        data = {'form': MaterialForm(instance=material)} 
    
    return render( request, 'transporte/editarmaterial.html', data)

# FORMULARIO VEHICULO

@login_required(login_url='login')
def AgregarVehiculo(request):
    vehiculo = Vehiculo.objects.all()
    for v in vehiculo:
        v.ruta = 1 if Ruta.objects.filter(vehiculo=v.id).exists() else 0
        if v.fechavencisoat < date.today():
            v.soat = 'Vencido'
        else:
            dias = (v.fechavencisoat - date.today()).days
            v.soat = f'Vigente - faltan {dias} días'

        if v.fechavencitecno < date.today():
            v.tecno = 'Vencido'
        else:
            dias = (v.fechavencitecno - date.today()).days
            v.tecno = f'Vigente - faltan {dias} días'     


    data = {'form': VehiculoForm,
            'vehiculo': vehiculo}

    if request.method == 'POST':
        formulario = VehiculoForm(request.POST)
        if formulario.is_valid():            
                formulario.save()
                return redirect('vehiculo')
        else:
            data['alerta'] = formulario.errors
            print(formulario.errors)

        data['form'] = formulario        

    return render(request, 'transporte/vehiculo.html', data)

@login_required(login_url='login')
def eliminarvehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()

    return redirect(AgregarVehiculo)

@login_required(login_url='login')
def edicionvehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    editar = 1
    data = {'form': VehiculoForm(instance=vehiculo),
            'editar': editar}

    if request.method == 'POST':
        formulario = VehiculoForm(request.POST, instance=vehiculo)
        if formulario.is_valid():
            formulario.save()
            return redirect('vehiculo')        
        else: 
            data = {'form': VehiculoForm(instance=vehiculo),
                'editar': editar} 
    
    return render( request, 'transporte/editarvehiculo.html', data)

@login_required(login_url='login')
def vervehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    editar = 0
    if vehiculo is not None:
        if vehiculo.fechavencisoat < date.today():
            vehiculo.soat = 'Vencido'
        else:
            dias = (vehiculo.fechavencisoat - date.today()).days
            vehiculo.soat = f'Vigente - faltan {dias} días'

        if vehiculo.fechavencitecno < date.today():
            vehiculo.tecno = 'Vencido'
        else:
            dias = (vehiculo.fechavencitecno - date.today()).days
            vehiculo.tecno = f'Vigente - faltan {dias} días' 

    data = {'form': VehiculoForm(instance=vehiculo),
            'editar': editar,
            'vehiculo': vehiculo}    
    return render( request, 'transporte/editarvehiculo.html', data)

@login_required(login_url='login')
def ruta(request):
    rutas = Ruta.objects.all()
    for r in rutas:
        if r.estado == 0:
            r.estadonombre = 'Pendiente'
        elif r.estado == 1:  
            r.estadonombre = 'Ruta Iniciada'
        else:
            r.estadonombre = 'Ruta Terminada'    

    data = {'rutas': rutas}   
    return render( request, 'transporte/ruta.html', data)

# FORMULARIO RUTA

@login_required(login_url='login')
def agregarruta(request):
    estado = 2
    data = {
        'form': RutaForm,
        'form2': RutaMaterialForm,
        'estado': estado
    }

    if request.method == 'POST':
        # Procesar el formulario de Ruta
        ruta_form = RutaForm(request.POST)
        
        if ruta_form.is_valid():
            # Guardar la instancia de Ruta
            pesototal_str = request.POST.get('txtPesoTotal')
            try:
                pesototal = float(pesototal_str)
            except ValueError:
                pesototal = None
            
            datos_tabla_json = request.POST.get('datos_tabla')
            datos_tabla = json.loads(datos_tabla_json)
             
            if  datos_tabla:
                if pesototal <= 1000:
                    ruta = ruta_form.save()                    
                    vehiculo = Vehiculo.objects.filter(pk=ruta.vehiculo.id).first()
                    vehiculo.SwAtive = 0
                    vehiculo.save()
                    usuario = CustomUser.objects.filter(pk=ruta.usuario.id).first()
                    usuario.SwAtive = 0
                    usuario.save()
                    # Procesar los materiales y unidades agregados temporalmente
                    
                    preciototal = 0
                    for dato in datos_tabla:
                        material_id = dato['materialId']
                        unidad = dato['unidades']
                        material = get_object_or_404(Material, id=material_id)
                        unidad = Decimal(unidad)
                        pesounidad = Decimal(material.pesounidad)
                        km = Decimal(ruta.km)                        
                        resultado_multiplicacion = 800000 * unidad * pesounidad * km
                        resultado_redondeado = resultado_multiplicacion.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        precio = resultado_redondeado / 5
                        precio = precio.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        Rutamaterial.objects.create(ruta=ruta, material=material, Unidades=unidad)                        
                        preciototal += precio

                    ruta.valortotal = preciototal
                    ruta.save()
                    # Redireccionar a algún lugar después de guardar
                    return redirect('ruta')
                else:
                    data['form'] = ruta_form
                    data['alerta'] = 'El peso total no puede sobrepasar los 1000 kg'                                  
            else:
                data['form'] = ruta_form
                data['alerta'] = 'No has agregado ningún material'
                
        else:
            data['alerta'] = ruta_form.errors 
            print(ruta_form.errors)
    

    return render(request, 'transporte/editarruta.html', data)

@login_required(login_url='login')
def obtener_km(request):
    ciudad_id = request.GET.get('ciudad_id')
    ciudad = Ciudad.objects.get(pk=ciudad_id)
    km = ciudad.km if ciudad else None
    return JsonResponse({'km': km})

@login_required(login_url='login')
def obtener_peso_material(request):
    if request.method == 'GET' and 'material_id' in request.GET:
        material_id = request.GET['material_id']
        try:
            material = Material.objects.get(id=material_id)
            return JsonResponse({'peso': material.pesounidad})
        except Material.DoesNotExist:
            return JsonResponse({'error': 'El material no existe.'}, status=404)
    else:
        return JsonResponse({'error': 'Se esperaba un ID de material válido.'}, status=400)

@login_required(login_url='login')
def verruta(request, id):
    ruta = get_object_or_404(Ruta.objects.prefetch_related('usuario','vehiculo'), id=id) 
    ruta.conductor = ruta.usuario.first_name + ' ' + ruta.usuario.last_name 
    ruta.placa = ruta.vehiculo.placa
    estado = 0       

    data = {'form': RutaForm(instance=ruta),
            'estado': estado,
            'rutaid': ruta.id,
            'ruta': ruta,
            }    
    return render( request, 'transporte/editarruta.html', data)


@login_required(login_url='login')
def obtener_datos_ruta_material(request):
    if request.method == 'GET' and 'rutaId' in request.GET:
        rutaId = request.GET['rutaId']
        
        datos_ruta_material = Rutamaterial.objects.filter(ruta_id=rutaId)       
        datos_ruta_material = datos_ruta_material.annotate(materialNombre=F('material__nombre'))
        datos_ruta_material = datos_ruta_material.annotate(km=F('ruta__km'))
        datos_ruta_material = datos_ruta_material.annotate(pesoMaterial=F('material__pesounidad'))
        datos_ruta_material = list(datos_ruta_material.values())
        return JsonResponse(datos_ruta_material, safe=False)

@login_required(login_url='login')    
def edicionruta(request, id):
    ruta = get_object_or_404(Ruta.objects.prefetch_related('usuario','vehiculo'), id=id) 
    ruta.conductor = ruta.usuario.first_name + ' ' + ruta.usuario.last_name 
    ruta.placa = ruta.vehiculo.placa
    estado = 1
    data = {'form': RutaForm(instance=ruta),
            'form2': RutaMaterialForm,
            'estado': estado,
            'rutaid': ruta.id,
            'ruta': ruta}
        
    if request.method == 'POST':        
        # Procesar el formulario de Ruta
        datos_tabla_json = request.POST.get('datos_tabla')
        datos_tabla = json.loads(datos_tabla_json)

        for dato in datos_tabla:
            km_str = dato['km']

        km_decimal = Decimal(km_str)
        km_decimal = km_decimal.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        request.POST._mutable = True
        request.POST['km'] = km_decimal
        request.POST['usuario'] = ruta.usuario.pk
        request.POST['vehiculo'] = ruta.vehiculo.pk        
        request.POST._mutable = False
        ruta_form = RutaForm(request.POST, instance=ruta)
        ruta_form.fields['usuario'].queryset = CustomUser.objects.all()
        ruta_form.fields['vehiculo'].queryset = Vehiculo.objects.all()       
        if ruta_form.is_valid():
            # Guardar la instancia de Ruta
            pesototal_str = request.POST.get('txtPesoTotal')
            try:
                pesototal = float(pesototal_str)
            except ValueError:
                pesototal = None

            if datos_tabla:
                if pesototal <= 1000:
                    ruta = ruta_form.save()
                    Rutamaterial.objects.filter(ruta=ruta).delete()

                    # Procesar los materiales y unidades agregados temporalmente
                    preciototal = 0
                    for dato in datos_tabla:
                        material_id = dato['materialId']
                        unidad = dato['unidades']
                        material = get_object_or_404(Material, id=material_id)
                        unidad = Decimal(unidad)
                        pesounidad = Decimal(material.pesounidad)
                        km = Decimal(ruta.km)                        
                        resultado_multiplicacion = 800000 * unidad * pesounidad * km
                        resultado_redondeado = resultado_multiplicacion.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        precio = resultado_redondeado / 5
                        precio = precio.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        Rutamaterial.objects.create(ruta=ruta, material=material, Unidades=unidad)                        
                        preciototal += precio

                    ruta.valortotal = preciototal
                    ruta.save()

                    # Redireccionar a algún lugar después de guardar
                    return redirect('ruta')
                else:
                    data['form'] = ruta_form
                    data['alerta'] = 'El peso total no puede sobrepasar los 1000 kg'                                  
            else:
                data['form'] = ruta_form
                data['alerta'] = 'No has agregado ningún material'      
        else:
            data['alerta'] = ruta_form.errors 
            print(ruta_form.errors)    
    
    return render( request, 'transporte/editarruta.html', data)    
        
@login_required(login_url='login')
def eliminarruta(request, id):
    Rutamaterial.objects.filter(ruta=id).delete()
    ruta = get_object_or_404(Ruta, id=id)
    ruta.delete()

    return redirect('ruta')

# RUTA CONDUCTOR

@login_required(login_url='login')
def rutaconductor(request):
    rutaconsulta = Ruta.objects.filter(
        Q(usuario=request.user.id),
        Q(estado=0) | Q(estado=1)
    ).first()
    if rutaconsulta:    
        ruta = get_object_or_404(Ruta.objects.prefetch_related('usuario','vehiculo'), Q(usuario=request.user.id), Q(estado=0) | Q(estado=1)) 
        ruta.conductor = ruta.usuario.first_name + ' ' + ruta.usuario.last_name 
        ruta.placa = ruta.vehiculo.placa    

        data = {'form': RutaForm(instance=ruta),
                'rutaid': ruta.id,
                'ruta': ruta,
                }    
        
        if ruta.estado == 1:
            data['alerta'] = 'Se a iniciado la Ruta Correctamente'
    else:
        data = {'alerta': 'No tienes ninguna Ruta asignada',}        

    return render( request, 'transporte/rutaconductor.html', data)

@login_required(login_url='login')
def estadorutainiciada(request):
    ruta = Ruta.objects.filter(usuario=request.user.id, estado=0).first()
    if ruta:
        ruta.estado = 1
        ruta.save()

    return redirect('rutaconductor')

@login_required(login_url='login')
def estadorutaterminada(request):
    ruta = Ruta.objects.filter(usuario=request.user.id, estado=1).first()
    if ruta:
        ruta.estado = 2
        ruta.save()
        vehiculo = Vehiculo.objects.filter(pk=ruta.vehiculo.id).first()
        vehiculo.SwAtive = 1
        vehiculo.save()
        usuario = CustomUser.objects.filter(pk=ruta.usuario.id).first()
        usuario.SwAtive = 1
        usuario.save()


    return redirect('rutaconductor')

# REPORTES

@login_required(login_url='login')
def reportes(request):

    return render(request,'transporte/reportes.html')   

@login_required(login_url='login')
def reporterutas(request):
        
        data = Ruta.objects.select_related('usuario', 'vehiculo').filter((Q(estado=0) | Q(estado=1)))
        for d in data:
            d.materiales = ''
            rutamaterial = Rutamaterial.objects.select_related('material').filter(ruta=d.id)
            for  r in rutamaterial:
                resultado = re.search(r.material.nombre, d.materiales, re.IGNORECASE)
                if not resultado:
                    d.materiales = d.materiales + r.material.nombre + ' - ' 
                
        xlsx = XlsGenerator(str(request.user), ['Logs',], 'NAME_APP')
        fields = ['Vehículo_Placa', 'Conductor', 'Materiales']
        body = [{'Vehículo_Placa': d.vehiculo.placa, 
                 'Conductor': d.usuario.first_name + ' ' + d.usuario.last_name,
                 'Materiales': d.materiales, } for d in data]
        title = 'Reporte de Registros (Logs)'

        work_book = xlsx.generate_table_simple(fields=fields, body=body,
                                                title=title, header=True,
                                                footer=False)
        if work_book and work_book['code'] == 200:
            filename = 'reporte_logs_calidad.xlsx'
            response = HttpResponse(content_type="application/ms-excel")
            contenido = "attachment; filename={0}".format(filename)
            response["Content-Disposition"] = contenido
            work_book['data'].save(response)
            return response
        messages.warning(request, 'No se puede generar el informe')
        return render(request,'transporte/reportes.html')  

@login_required(login_url='login')
def reportematerial(request):

    return redirect('reportes')

@login_required(login_url='login')
def reportevehiculos(request):

    return redirect('reportes')    

