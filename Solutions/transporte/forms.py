from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Rol, Tipodocumento, Material, Vehiculo, Ciudad, Ruta, Rutamaterial
from django.core.validators import MaxValueValidator
from django.db.models import Q, F
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    documento = forms.CharField(max_length=20)
    telefono = forms.CharField(max_length=15, required=False)   
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    email = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    tipodocumento = forms.ModelChoiceField(queryset=Tipodocumento.objects.all())
    licencia = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'oculto'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'tipodocumento', 'documento', 'telefono', 'rol' , 'licencia', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'

        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Apellido'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['documento'].widget.attrs['placeholder'] = 'documento'
        self.fields['telefono'].widget.attrs['placeholder'] = 'telefono'
        self.fields['licencia'].widget.attrs['placeholder'] = 'licencia'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
    
class MaterialForm(forms.ModelForm):
    nombre = forms.CharField(max_length=255, required=True)
    presentacion = forms.CharField(max_length=255, required=True)  
    pesounidad = forms.DecimalField(decimal_places=2, max_digits=20, required=True)  

    class Meta:
        model = Material
        fields = ['nombre', 'presentacion', 'pesounidad']

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'

        self.fields['nombre'].widget.attrs['placeholder'] = 'Material'
        self.fields['presentacion'].widget.attrs['placeholder'] = 'Presentación'
        self.fields['pesounidad'].widget.attrs['placeholder'] = 'Peso (Kg)'  

class VehiculoForm(forms.ModelForm):
    placa = forms.CharField(max_length=255, required=True)
    marca = forms.CharField(max_length=255, required=True)
    modelo = forms.CharField(max_length=255, required=True) 
    year = forms.IntegerField(validators=[MaxValueValidator(limit_value=9999)], required=True) 
     
    fechavencisoat = forms.DateField(required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha Vencimiento Soat','readonly':True}),
    )  
    fechavencitecno = forms.DateField(required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha Vencimiento Tecnomecánica','readonly':True}),
    ) 

    class Meta:
        model = Vehiculo
        fields = ['placa', 'marca', 'modelo', 'year', 'fechavencisoat', 'fechavencitecno']
   

    def __init__(self, *args, **kwargs):
        super(VehiculoForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'

        self.fields['placa'].widget.attrs['placeholder'] = 'Placa'
        self.fields['marca'].widget.attrs['placeholder'] = 'Marca'
        self.fields['modelo'].widget.attrs['placeholder'] = 'Modelo'           

class RutaForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=CustomUser.objects.filter(
        Q(rol=2) & (Q(SwAtive=1))
    ), required=True)
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all(), required=True)
    km = forms.DecimalField(decimal_places=2, max_digits=20, required=True)   
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.filter(
        (Q(SwAtive=1)) &
        Q(fechavencisoat__gt=date.today()) &
        Q(fechavencitecno__gt=date.today())
    ), required=True) 

    class Meta:
        model = Ruta
        fields = ['usuario', 'ciudad', 'km', 'vehiculo']

    def __init__(self, *args, **kwargs):
        super(RutaForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'

        self.fields['km'].widget.attrs['placeholder'] = 'Km'  

class RutaMaterialForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all(), required=False)
    Unidades = forms.IntegerField(required=False) 

    class Meta:
        model = Rutamaterial
        fields = ['material', 'Unidades']

    def __init__(self, *args, **kwargs):
        super(RutaMaterialForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control'

        self.fields['Unidades'].widget.attrs['placeholder'] = 'Unidades'               