from django import forms
from .models import Producto, Venta, ProductoVenta, Suministro, Devolucion
from django.utils import timezone
from django.contrib.auth.models import User
class DateInput(forms.DateInput):
    input_type = 'date'

class AñadirProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock']
        labels = {
            'nombre': 'Nombre',
            'precio': 'Precio',
            'stock': 'Stock',
        }
        widgets = { 
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            
        }

from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password': 'Contraseña',
        }



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            
        }


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)



class VentaForm(forms.ModelForm):
    metodo_de_pago = forms.ChoiceField(choices=Venta.METODOS_DE_PAGO, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Venta
        exclude = ['fecha_venta']

class VentasProductoForm(forms.ModelForm):
    cantidad_producto = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control', 'step': 'any'}))
    class Meta:
        model = ProductoVenta
        fields = ['producto', 'cantidad_producto']
        labels = {
            'producto': 'Producto',
            'cantidad_producto': 'Cantidad',
    
        }
        widgets = {
            'producto': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

        

class Suministroform(forms.ModelForm):
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = Suministro
        fields = ['nombre_producto', 'cantidad','proveedor', 'precio_unitario', ]
        labels = {
            'nombre_producto': 'Nombre Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
           
            'proveedor': 'Proveedor',
        }
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.TextInput(attrs={'class':'form-control'}),
            'proveedor': forms.TextInput(attrs={'class':'form-control'}),
            
            'precio_unitario': forms.NumberInput(attrs={'class':'form-control'}),
        }

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields = [ 'razon', 'comentarios']
        widgets = {
            
            'razon': forms.RadioSelect(),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }

class FiltrarVentasForm(forms.Form):
    fecha_inicio = forms.DateField(label="Fecha de inicio", required=False, widget=DateInput())
    fecha_fin = forms.DateField(label="Fecha de fin", required=False, widget=DateInput())

    
class BuscarVentaForm(forms.Form):
        model = Venta
        id_venta = forms.IntegerField(
        label='Buscar por id de venta',
        widget=forms.NumberInput(attrs={'placeholder': 'Introduce el ID de la venta'})
    )
