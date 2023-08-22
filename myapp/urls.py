from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy




urlpatterns = [
    path('', views.user_login),
    path('inventario/', views.inventario, name='inventario'),
    path('historial/', views.historial),
    path('devoluciones/', views.devoluciones , name='devoluciones'),
    path('ventas/', views.ventas),
    path('ventas/', views.ventas, name='ventas'),
    path('proveedores/',views.proveedores),
    path('cuenta/',views.cuenta),
    path('ventas_pdf/', views.ventas_pdf, name='ventas_pdf'),
    path('manage_account/', views.manage_account, name='manage_account'),
    path('inventario/eliminar/<int:id_producto>/', views.inventario, name='eliminar_producto'),
    path('inventario/editar/<int:id_producto>/', views.inventario, name='editar_producto'),
    path('checkout/', views.checkout),
    path('add_suministro/', views.add_suministro, name='add_suministro'),
    path('buscar_venta/', views.buscar_venta, name='buscar_venta'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
     path('buscar_ventas/', views.buscar_ventas, name='buscar_ventas'),
     path('procesar_devolucion/<int:id_venta>/', views.procesar_devolucion, name='procesar_devolucion'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),





]

