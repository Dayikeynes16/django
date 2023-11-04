from django.contrib import admin
from .models import  Producto, Venta, Suministro, Devolucion, ProductoVenta

# Register your models here.

admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Suministro)
admin.site.register(Devolucion)
admin.site.register(ProductoVenta)


