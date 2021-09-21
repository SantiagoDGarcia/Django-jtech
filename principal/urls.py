from django.urls import path
from principal.views import *

urlpatterns = [
      # Telefono
      path('', index, name='index'),
      path('telefonos', telefonos, name='telefonos'),
      path('anadir-telefono', crear_telefono, name='crear_telefono'),
      path('editar-telefono/<int:id>', editar_telefono, name='editar_telefono'),
      path('eliminar-telefono/<int:id>', eliminar_telefono, name='eliminar_telefono'),
      # Monedero
      path('monedero/<int:id>', monedero, name='monedero'),
      path('anadir-al-monedero-transaccion/<int:id>', monedero_transaccion, name='monedero_transaccion'),
      path('anadir-al-monedero-telefono/<int:id>', monedero_telefono, name='monedero_telefono'),
      path('anadir-al-monedero-dispositivo/<int:id>', monedero_dispositivo, name='monedero_dispositivo'),
      path('anadir-al-monedero-accesorio/<int:id>', monedero_accesorio, name='monedero_accesorio'),
      path('eliminar-del-monedero-transaccion/<int:id>/<int:mn>', eliminar_transaccion, name='eliminar_transaccion'),
      # Dispositivos
      path('dispositivos', dispositivos, name='dispositivos'),
      path('anadir-dispositivo', crear_dispositivo, name='crear_dispositivo'),
      path('editar-dispositivo/<int:id>', editar_dispositivo, name='editar_dispositivo'),
      path('eliminar-dispositivo/<int:id>', eliminar_dispositivo, name='eliminar_dispositivo'),
      # Accesorios
      path('anadir-accesorio', crear_accesorio, name='crear_accesorio'),
      path('editar-accesorio/<int:id>', editar_accesorio, name='editar_accesorio'),
      path('eliminar-accesorio/<int:id>', eliminar_accesorio, name='eliminar_accesorio'),
      # Urls para el logeo
      path('login/', ingreso, name="ingreso"), 
      path('deslogeo/', salida, name="salida"),
]
