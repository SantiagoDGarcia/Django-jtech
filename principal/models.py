from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class Telefono(models.Model):
      # Se usa para definir un orden o su verbo en plural
      class Meta:
            ordering = ["modelo"]
            verbose_name_plural = "Teléfonos"
            
      opciones_modalidad = ( ('Open box', 'Open box'), ('Sellado', 'Sellado'), )
      modalidad = models.CharField(max_length=10, choices=opciones_modalidad, default='Open box')
      opciones_capacidad = ( ('16GB', '16GB'), ('32GB', '32GB'), ('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB'), ('512GB', '512GB'), )
      capacidad = models.CharField(max_length=5, choices=opciones_capacidad)
      modelo =  models.ForeignKey('ModeloTelefono', on_delete=models.CASCADE, related_name="modelos")
      
      imei = models.BigIntegerField()
      imei2 = models.BigIntegerField(blank=True, null=True)
      color = models.CharField(max_length=20)
      bateria = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
      fecha_venta = models.DateField(blank=True, null=True)
      fecha_compra = models.DateField(default=datetime.date.today())
      proveedor = models.CharField(max_length=50)
      cliente = models.CharField(max_length=50, blank=True, null=True)
      nro_cliente = models.CharField(max_length=15, blank=True, null=True)
      monto_compra = models.FloatField(blank=True, null=True, default=0)
      monto_venta = models.FloatField(blank=True, null=True)
      vendido = models.BooleanField(default=False)
      opciones_entrega = ( ('Entregado', 'Entregado'), ('Envio servientrega', 'Envio servientrega'), ('Envio cooperativa','Envio cooperativa') )
      entrega = models.CharField(max_length=20, choices=opciones_entrega, default='Entregado', null=True, blank=True)
      
      llego_cargador = models.BooleanField( default=False)
      llego_cargador_rapido = models.BooleanField( default=False)
      llego_audifonos = models.BooleanField(default=False)
      
      sefue_cargador = models.BooleanField( default=False)
      sefue_cargador_rapido = models.BooleanField( default=False)
      sefue_audifonos = models.BooleanField(default=False)
      
      precio_cargador = models.DecimalField(blank=True, null=True, default=5.5 ,decimal_places=2, max_digits=5)
      precio_cargador_rapido = models.DecimalField(blank=True, null=True, default=13, decimal_places=2, max_digits=5)
      precio_audifonos = models.DecimalField(blank=True, null=True, default=5, decimal_places=2, max_digits=5)
      
      monederos = models.ManyToManyField('Monedero', through='Transaccion')

      # Metodo de presentacion textual de objetos
      def __str__(self):
            return "%s - %s - %s" % (self.modelo,
                  self.modalidad,
                  self.capacidad)
      def valor_total_transacciones(self):
            valor = [x.dinero for x in self.transacciones.all() ]
            return sum(valor)   
      def precios_accesorios(self):
            if self.sefue_cargador:
                  if self.llego_cargador:
                        val1 = 0
                  else: 
                        val1=self.precio_cargador
            else :
                  val1=0
            
            if self.sefue_cargador_rapido:
                  if self.llego_cargador_rapido:
                        val2 = 0
                  else: 
                        val2=self.precio_cargador_rapido
            else :
                  val2=0
                  
            if self.sefue_audifonos:
                  if self.llego_audifonos:
                        val3 = 0
                  else: 
                        val3=self.precio_audifonos
            else :
                  val3=0
                  
            return (val1+val2+val3)
      def ganancia(self):
            ganancia = 0
            if self.monto_venta:
                  ganancia = self.monto_venta - self.monto_compra - float(self.precios_accesorios())
            return "%.2f" % ganancia
      
      def dinero_disponible_transaccion(self):
            money = self.monto_venta  - float( self.valor_total_transacciones())
            return money
            
class ModeloTelefono(models.Model):
      class Meta:
            ordering = ["marca", "nombre"]
            verbose_name_plural = "Modelos de teléfono"
      nombre = models.CharField(max_length=50)
      opciones_marca = ( ('Samsung', 'Samsung'), ('Apple', 'Apple'), )
      marca = models.CharField(max_length=15, choices=opciones_marca, default='Apple')
      def __str__(self):
            return "%s" % (self.nombre)
      
class Monedero(models.Model):
      class Meta:
            ordering = ["nombre"]
            verbose_name_plural = "Monederos"
      nombre = models.CharField(max_length=50, unique=True)
      descripcion = models.CharField(max_length=50, null=True, blank=True)
      
      telefonos = models.ManyToManyField(Telefono, through='Transaccion')
      dispositivos = models.ManyToManyField('Dispositivo', through='Transaccion')
      accesorios = models.ManyToManyField('Accesorio', through='Transaccion')
      def __str__(self):
            return "%s" % (self.nombre)
      # Metodo generico para obtener informacion
      def obtener_dinero_caja(self):
            valor = [x.dinero for x in self.transacciones.all() ]
            return sum(valor)
      
class Transaccion(models.Model):
      class Meta:
            ordering = ["fecha"]
            verbose_name_plural = "Transacciones"
      telefono = models.ForeignKey(Telefono, related_name='transacciones', on_delete=models.CASCADE, blank=True, null=True)
      monedero = models.ForeignKey(Monedero, related_name='transacciones', on_delete=models.CASCADE)
      
      dispositivo = models.ForeignKey('Dispositivo', related_name='transacciones', on_delete=models.CASCADE, blank=True, null=True)
      accesorio = models.ForeignKey('Accesorio', related_name='transacciones', on_delete=models.CASCADE, blank=True, null=True)
      
      fecha = models.DateField(default=datetime.date.today() )
      hora = models.TimeField(default=datetime.datetime.now().time() )
      opciones_tipo = ( ('Efectivo', 'Efectivo'), ('Transferencia banco', 'Transferencia banco'),  ('Tarjeta de crédito', 'Tarjeta de crédito'), )
      tipo = models.CharField(max_length=20, choices=opciones_tipo, default='Efectivo')
      motivo = models.CharField(max_length=100, null=True, blank=True, default="Ninguno")
      
      dinero = models.FloatField(default=0)
      # Metodo de presentacion textual de objetos
      def __str__(self):
            return "%s - %s - %s" % (self.fecha, self.monedero, self.telefono)
      
      
class Accesorio(models.Model):
      class Meta:
            ordering = ["marca", "tipo"]
            verbose_name_plural = "Accesorios"
      opciones_marca = ( ('Samsung', 'Samsung'), ('Apple', 'Apple'), ('Xiaomi', 'Xiaomi'), ('Otro', 'Otro') )
      marca = models.CharField(max_length=15, choices=opciones_marca, default='Apple')
      opciones_tipo = ( ('Cargador', 'Cargador'), ('Cable', 'Cable'), ('Adaptador', 'Adaptador'), ('Audífonos', 'Audífonos'), ('Protector', 'Protector'), ('Mica', 'Mica'), ('Otro', 'Otro'), )
      tipo = models.CharField(max_length=15, choices=opciones_tipo, default='Cargador')
      opciones_conexion = ( ('Lightning', 'Lightning'), ('Tipo C', 'Tipo C'), ('Micro USB', 'Micro USB'), ('Inalámbrica', 'Inalámbrica'), ('Otra', 'Otra'), )
      conexion = models.CharField(max_length=15, choices=opciones_conexion, default='Lightning', null=True, blank=True)
      descripcion = models.CharField(max_length=50, default="")

      fecha_compra = models.DateField(blank=True, null=True)
      fecha_venta = models.DateField(default=datetime.date.today())
      
      proveedor = models.CharField(max_length=50, blank=True, null=True)
      cliente = models.CharField(max_length=50, blank=True, null=True)
      nro_cliente = models.CharField(max_length=15, blank=True, null=True)
      
      monto_compra = models.FloatField(default=0)
      monto_venta = models.FloatField()

      opciones_entrega = ( ('Entregado', 'Entregado'), ('Envio servientrega', 'Envio servientrega'), ('Envio cooperativa','Envio cooperativa') )
      entrega = models.CharField(max_length=20, choices=opciones_entrega, default='Entregado', null=True, blank=True)
      
      monederos = models.ManyToManyField('Monedero', through='Transaccion')

      # Metodo de presentacion textual de objetos
      def __str__(self):
            return "%s %s" % (self.tipo, self.conexion)
      def valor_total_transacciones(self):
            valor = [x.dinero for x in self.transacciones.all() ]
            return sum(valor)
      def ganancia(self):
            ganancia = 0
            if self.monto_venta:
                  ganancia = self.monto_venta - self.monto_compra
            return "%.2f" % ganancia
      def dinero_disponible_transaccion(self):
            money = self.monto_venta  - float( self.valor_total_transacciones())
            return money
      
      
class Dispositivo(models.Model):
      # Se usa para definir un orden o su verbo en plural
      class Meta:
            ordering = ["modelo"]
            verbose_name_plural = "Dispositivos"
            
      opciones_modalidad = ( ('Open box', 'Open box'), ('Sellado', 'Sellado'), )
      modalidad = models.CharField(max_length=10, choices=opciones_modalidad, default='Open box')
      opciones_capacidad = ( ('8GB', '8GB'),('16GB', '16GB'),('32GB', '32GB'),('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB'), ('512GB', '512GB'), ('1TB', '1TB'), ('2TB', '2TB') )
      capacidad = models.CharField(max_length=5, choices=opciones_capacidad)
      modelo =  models.ForeignKey('ModeloDispositivo', on_delete=models.CASCADE, related_name="modelos")
      tamanio = models.FloatField(default=11)
            
      imei = models.IntegerField(blank=True, null=True)
      serial = models.CharField(max_length=20, blank=True, null=True)
      
      color = models.CharField(max_length=20, blank=True, null=True)
      fecha_compra = models.DateField(default=datetime.date.today())
      fecha_venta = models.DateField(blank=True, null=True)
      
      proveedor = models.CharField(max_length=50, blank=True, null=True )
      cliente = models.CharField(max_length=50, blank=True, null=True)
      nro_cliente = models.CharField(max_length=15, blank=True, null=True)
      monto_compra = models.FloatField(null=True, blank=True, default=0)
      monto_venta = models.FloatField(blank=True, null=True)
      vendido = models.BooleanField(default=False)
      
      descripcion = models.CharField(max_length=50)
      
      opciones_entrega = ( ('Entregado', 'Entregado'), ('Envio servientrega', 'Envio servientrega'), ('Envio cooperativa','Envio cooperativa') )
      entrega = models.CharField(max_length=20, choices=opciones_entrega, default='Entregado', null=True, blank=True)
      
      llego_cargador = models.BooleanField( default=False)
      llego_audifonos = models.BooleanField(default=False)
      
      sefue_cargador = models.BooleanField( default=False)
      sefue_audifonos = models.BooleanField(default=False)
      precio_cargador = models.DecimalField(blank=True, null=True, default=5.5 ,decimal_places=2, max_digits=5)
      precio_audifonos = models.DecimalField(blank=True, null=True, default=5, decimal_places=2, max_digits=5)
      
      monederos = models.ManyToManyField('Monedero', through='Transaccion')

      # Metodo de presentacion textual de objetos
      def __str__(self):
            return "%s - %s - %s" % (self.modelo,
                  self.modalidad,
                  self.capacidad)
      def valor_total_transacciones(self):
            valor = [x.dinero for x in self.transacciones.all() ]
            return sum(valor)
      def precios_accesorios(self):
            if self.sefue_cargador:
                  if self.llego_cargador:
                        val1 = 0
                  else: 
                        val1=self.precio_cargador
            else :
                  val1=0
                              
            if self.sefue_audifonos:
                  if self.llego_audifonos:
                        val3 = 0
                  else: 
                        val3=self.precio_audifonos
            else :
                  val3=0
                  
            return (val1+val3)
      def ganancia(self):
            ganancia = 0
            if self.monto_venta:
                  ganancia = self.monto_venta - self.monto_compra - float(self.precios_accesorios())
            return "%.2f" % ganancia
      def dinero_disponible_transaccion(self):
            money = self.monto_venta  - float( self.valor_total_transacciones())
            return money


class ModeloDispositivo(models.Model):
      class Meta:
            ordering = ["marca", "nombre"]
            verbose_name_plural = "Modelos de dispositivos"
      nombre = models.CharField(max_length=30)
      opciones_marca = ( ('Samsung', 'Samsung'), ('Apple', 'Apple'), ('Otra', 'Otra'))
      marca = models.CharField(max_length=15, choices=opciones_marca, default='Apple')

        # Metodo de presentacion textual de objetos
      def __str__(self):
            return "%s" % (self.nombre)