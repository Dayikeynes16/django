from django.db import models
import random
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime


    

def generar_id_venta():
    return random.randint(10000, 99999)



class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nombre + " " 




class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True, default=generar_id_venta)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    abierta = models.BooleanField(default=True)
    METODOS_DE_PAGO = (
    ('tarjeta', 'Tarjeta'),
    ('transferencia', 'Transferencia'),
    ('efectivo', 'Efectivo'),
)

    metodo_de_pago = models.CharField(max_length=15, choices=METODOS_DE_PAGO, default='efectivo')



    def __str__(self):
        return f"Venta #{self.id_venta}"

    def save(self, *args, **kwargs):
        # Calcula el total de la venta
        self.total = sum([p.subtotal_producto for p in self.productoventa_set.all()])
        self.METODOS_DE_PAGO = self.metodo_de_pago
        super(Venta, self).save(*args, **kwargs)

    


class ProductoVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad_producto = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal_producto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.precio = self.producto.precio
        self.subtotal_producto = self.cantidad_producto * self.precio
        super(ProductoVenta, self).save(*args, **kwargs)

class Suministro(models.Model):
    id_suministro = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=30)
    proveedor = models.CharField(max_length=30)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def save(self, *args, **kwargs):
        self.total = self.precio_unitario * self.cantidad
        super(Suministro, self).save(*args, **kwargs)
    def __str__(self):
        return self.nombre_producto + " " 
    

class Devolucion(models.Model):
    id_devolucion = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(ProductoVenta, on_delete=models.CASCADE)

    RAZONES = (
        ('Producto en mal estado', 'Producto en mal estado'),
        ('exceso de grasa', 'Exceso de grasa'),
        ('producto equivocado', 'Producto equivocado'),
        ('otro', 'Otro'),
    )
    razon = models.CharField(max_length=35, choices=RAZONES, default='otro')
    fecha = models.DateTimeField(default=timezone.now)
    comentarios = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    


    def __str__(self):
        return f"Devolución de {self.producto} de la venta {self.venta.id_venta}"
    
