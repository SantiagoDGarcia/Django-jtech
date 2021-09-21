from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from principal.models import Telefono, Monedero, Transaccion, Dispositivo, Accesorio

import datetime

# Formularios principales
class FormTelefono(ModelForm):
      class Meta: 
            model = Telefono
            fields = ['modelo', 'capacidad', 'modalidad', 'imei', 'imei2', 'color', 'fecha_compra', 'monto_compra', 'proveedor', 
                      'vendido', 'fecha_venta', 'monto_venta' ,'cliente','bateria', 
                      'entrega' ,'llego_cargador', 'llego_cargador_rapido', 'llego_audifonos', 'sefue_cargador', 'sefue_audifonos' , 'sefue_cargador_rapido',
                      'precio_cargador', 'precio_cargador_rapido', 'precio_audifonos', 'nro_cliente']
            
      def clean_monto_venta(self):
            ingreso = self.cleaned_data['monto_venta']
            if  self.cleaned_data['vendido'] and (ingreso is None or ingreso == 0):
                  raise forms.ValidationError("El monto de venta no puede estar vacio o ser 0")
            return ingreso
      
      def clean_fecha_venta(self):
            ingreso = self.cleaned_data['fecha_venta']
            if ingreso is None and self.cleaned_data['vendido']:
                  raise forms.ValidationError("Se debe seleccionar una fecha válida")
            return ingreso
            
class FormMonedero(ModelForm):
      def __init__(self, monedero, *args, **kwargs):
            super(FormMonedero, self).__init__(*args, **kwargs)
            self.initial['monedero'] = monedero
            self.fields['monedero'].widget = forms.widgets.HiddenInput()
            self.initial['fecha'] = datetime.date.today()
            self.fields['fecha'].widget = forms.widgets.HiddenInput() 
            self.initial['hora'] = datetime.datetime.now().time()
            self.fields['hora'].widget = forms.widgets.HiddenInput()
      class Meta: 
            model = Transaccion
            fields = ['monedero', 'fecha', 'hora', 'dinero', 'tipo', 'motivo']
            
class FormDispositivo(ModelForm):
      class Meta: 
            model = Dispositivo
            #message = forms.CharField(widget=forms.Textarea)
            fields = ['modelo', 'capacidad', 'modalidad', 'imei', 'serial', 'color', 'fecha_compra', 'monto_compra', 'proveedor', 
                      'vendido',  'tamanio', 'fecha_venta', 'monto_venta' ,'cliente', 'descripcion',
                      'entrega' ,'llego_cargador', 'llego_audifonos', 'sefue_cargador', 'sefue_audifonos',
                      'precio_cargador', 'precio_audifonos', 'nro_cliente']
            
      def clean_monto_venta(self):
            ingreso = self.cleaned_data['monto_venta']
            if  self.cleaned_data['vendido'] and (ingreso is None or ingreso == 0):
                  raise forms.ValidationError("El monto de venta no puede estar vacio o ser 0")
            return ingreso
      
      def clean_fecha_venta(self):
            ingreso = self.cleaned_data['fecha_venta']
            if ingreso is None and self.cleaned_data['vendido']:
                  raise forms.ValidationError("Se debe seleccionar una fecha válida")
            return ingreso
            
class FormAccesorio(ModelForm):
      class Meta: 
            model = Accesorio
            fields = ['tipo', 'marca', 'conexion',  'monto_compra', 'fecha_venta', 'monto_venta' ,'cliente', 'descripcion',
                      'entrega', 'nro_cliente' ]
            
            
# Formularios secundarios
class FormMonederoTelefono(ModelForm):
      def __init__(self, telefono, *args, **kwargs):
            super(FormMonederoTelefono, self).__init__(*args, **kwargs)
            self.initial['telefono'] = telefono
            self.fields['telefono'].widget = forms.widgets.HiddenInput()
            self.initial['fecha'] = datetime.date.today()
            self.fields['fecha'].widget = forms.widgets.HiddenInput() 
            self.initial['hora'] = datetime.datetime.now().time()
            self.fields['hora'].widget = forms.widgets.HiddenInput()
      class Meta: 
            model = Transaccion
            fields = ['monedero', 'telefono', 'fecha', 'hora', 'dinero', 'tipo', 'motivo']
      
      def clean_dinero(self):
            ingreso = self.cleaned_data['dinero']
            if ingreso >self.initial['telefono'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            if ingreso+self.initial['telefono'].valor_total_transacciones() >self.initial['telefono'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            return ingreso

class FormMonederoTelefonoEdit(ModelForm):
      def __init__(self, telefono, monedero,*args, **kwargs):
            super(FormMonederoTelefonoEdit, self).__init__(*args, **kwargs)
            self.initial['telefono'] = telefono
            self.fields['telefono'].widget = forms.widgets.HiddenInput()
            self.initial['fecha'] = datetime.date.today()
            self.fields['fecha'].widget = forms.widgets.HiddenInput() 
            self.initial['hora'] = datetime.datetime.now().time()
            self.fields['hora'].widget = forms.widgets.HiddenInput()
            self.initial['monedero'] = monedero
            self.fields['monedero'].widget = forms.widgets.HiddenInput()
      class Meta: 
            model = Transaccion
            fields = ['monedero', 'telefono', 'fecha', 'hora', 'dinero', 'tipo', 'motivo']
      
      def clean_dinero(self):
            ingreso = self.cleaned_data['dinero']
            if ingreso >self.initial['telefono'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            if ingreso+self.initial['telefono'].valor_total_transacciones() >self.initial['telefono'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            return ingreso

class FormMonederoDispositivo(ModelForm):
      def __init__(self, dispositivo, *args, **kwargs):
            super(FormMonederoDispositivo, self).__init__(*args, **kwargs)
            self.initial['dispositivo'] = dispositivo
            self.fields['dispositivo'].widget = forms.widgets.HiddenInput()
            self.initial['fecha'] = datetime.date.today()
            self.fields['fecha'].widget = forms.widgets.HiddenInput() 
            self.initial['hora'] = datetime.datetime.now().time()
            self.fields['hora'].widgetf = forms.widgets.HiddenInput()
      class Meta: 
            model = Transaccion
            fields = ['monedero', 'dispositivo', 'fecha', 'hora', 'dinero', 'tipo', 'motivo']
      
      def clean_dinero(self):
            ingreso = self.cleaned_data['dinero']
            if ingreso >self.initial['dispositivo'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            if ingreso+self.initial['dispositivo'].valor_total_transacciones() >self.initial['dispositivo'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            return ingreso
      
class FormMonederoAccesorio(ModelForm):
      def __init__(self, accesorio, *args, **kwargs):
            super(FormMonederoAccesorio, self).__init__(*args, **kwargs)
            self.initial['accesorio'] = accesorio
            self.fields['accesorio'].widget = forms.widgets.HiddenInput()
            self.initial['fecha'] = datetime.date.today()
            self.fields['fecha'].widget = forms.widgets.HiddenInput() 
            self.initial['hora'] = datetime.datetime.now().time()
            self.fields['hora'].widget = forms.widgets.HiddenInput()
      class Meta: 
            model = Transaccion
            fields = ['monedero', 'accesorio', 'fecha', 'hora', 'dinero', 'tipo', 'motivo']
      
      def clean_dinero(self):
            ingreso = self.cleaned_data['dinero']
            if ingreso >self.initial['accesorio'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            if ingreso+self.initial['accesorio'].valor_total_transacciones() >self.initial['accesorio'].monto_venta:
                  raise forms.ValidationError("El valor sobrepasa el precio de venta")
            return ingreso