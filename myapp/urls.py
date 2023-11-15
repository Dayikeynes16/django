from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.user_login),
    path('inventario/', views.inventario, name='inventario'),
    path('historial/', views.historial),
    path('devoluciones/', views.devoluciones , name='devoluciones'),
    path('ventas/', views.ventas),
    path('ventas/', views.ventas, name='ventas'),
    path('mapa/', views.mapa),
    path('proveedores/',views.proveedores),
    path('pedidos/', views.pedidos),
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
    path('añadir-producto/', views.añadir_producto, name='añadir_producto'),
    path('editar-producto/',views.editar_producto, name="editar-producto"),
    path('procesar-codigo/', views.procesar_codigo_barras, name='procesar_codigo'),
     path('weather/', views.weather, name='weather'),
    path ('cliente/', views.cliente,  name = 'cliente'),
    path('editar_stock/<int:id_producto>/', views.edit_stock, name='edit_stock'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

