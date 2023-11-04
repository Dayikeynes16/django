from myapp.models import  Producto, Venta , Suministro, ProductoVenta, Devolucion
from django.shortcuts import render,redirect, get_object_or_404
from .form import AñadirProductoForm, VentaForm, VentasProductoForm, Suministroform, DevolucionForm, BuscarVentaForm, UserRegistrationForm, UserUpdateForm, PasswordChangeForm, BuscarVentaForm
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import FileResponse, JsonResponse
from django.db.models import Sum
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from reportlab.lib.units import inch
from django.conf import settings
import requests
import os


def ventas_pdf(request):
    buffer = BytesIO()
   

    response = FileResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ventas.pdf"'

    # Crear un objeto PDF con orientación horizontal
    p = canvas.Canvas(buffer, pagesize=letter)

    # Consultar los datos
    current_date = timezone.now().date() 
    start_date = current_date
    end_date = current_date + timezone.timedelta(days=1)
    ventas_del_dia = Venta.objects.filter(fecha__range=(start_date, end_date))
    total_vendido = ventas_del_dia.aggregate(Sum('total'))['total__sum'] or 0
    total_efectivo = ventas_del_dia.filter(metodo_de_pago='efectivo').aggregate(Sum('total'))['total__sum'] or 0
    total_tarjeta = ventas_del_dia.filter(metodo_de_pago='tarjeta').aggregate(Sum('total'))['total__sum'] or 0
    total_transferencia = ventas_del_dia.filter(metodo_de_pago='transferencia').aggregate(Sum('total'))['total__sum'] or 0
    print("Total Efectivo:", total_efectivo)

     # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2.5 * inch, 10.5 * inch, "Carnicería El Puebla - Reporte de Ventas Diario")
    p.setFont("Helvetica", 12)
    p.drawString(1 * inch, 10 * inch, f"Fecha: {current_date}")

    # Resumen de ventas
    data_resumen = [
        ["Total vendido", f"${total_vendido}"],
        ["Ventas en efectivo", f"${total_efectivo}"],
        ["Ventas con tarjeta", f"${total_tarjeta}"],
        ["Ventas por transferencia", f"${total_transferencia}"]
    ]
    table_resumen = Table(data_resumen, colWidths=[3 * inch, 2 * inch])
    table_resumen.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    table_resumen.wrapOn(p, 0, 0)
    table_resumen.drawOn(p, 1 * inch, 8.5 * inch)

    # Listado de ventas
    data_ventas = [["ID Venta", "Fecha", "Total", "Método de Pago"]]
    for venta in ventas_del_dia:
        data_ventas.append([venta.id_venta, venta.fecha, venta.total, venta.get_metodo_de_pago_display()])
    table_ventas = Table(data_ventas, colWidths=[1 * inch, 2 * inch, 2 * inch, 3 * inch])
    table_ventas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    table_ventas.wrapOn(p, 0, 0)
    table_ventas.drawOn(p, 1 * inch, 6 * inch - len(ventas_del_dia) * 0.25 * inch)

    # Finalizar el PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ventas.pdf"'

    return response 

@login_required
def ventas(request):

    productos = Producto.objects.all()

    venta_form = VentaForm(request.POST or None)  # Inicializamos por defecto
    ventas_producto_form = VentasProductoForm()  # Inicializamos por defecto

    # Obtiene la venta abierta actual (suponiendo que solo hay una a la vez).
    venta_actual = Venta.objects.filter(abierta=True).first()

    # Obtiene todos los productos asociados a esta venta.
    productos_venta = ProductoVenta.objects.filter(venta=venta_actual) if venta_actual else []

    if request.method == "POST":
       
        action = request.POST.get('action')

        
        if action == 'start_sale':
            Venta.objects.create()
            messages.success(request, "Nueva venta iniciada.")
            return redirect('ventas')

        elif action == 'remove_product':
            producto_venta_id = request.POST.get('producto_venta_id')
            producto_venta = get_object_or_404(ProductoVenta, id=producto_venta_id)

            # Updating the product stock
            producto = producto_venta.producto
            producto.stock += producto_venta.cantidad_producto
            producto.save()

            # Deleting the ProductoVenta
            producto_venta.delete()

            messages.success(request, f"Producto {producto.nombre} eliminado de la venta.")
            return redirect('ventas')

        elif action == 'add_product':
            ventas_producto_form = VentasProductoForm(request.POST)
            if ventas_producto_form.is_valid():
                ventas_producto = ventas_producto_form.save(commit=False)
                if not venta_actual:  # Si no hay una venta abierta, crea una.
                    venta_actual = Venta.objects.create()
                ventas_producto.venta = venta_actual

                # Actualización del stock del producto
                producto = ventas_producto.producto  # Obteniendo el producto asociado.
                if producto.stock < Decimal(ventas_producto.cantidad_producto):  # Verificando si hay suficiente stock.
                    messages.error(request, f"No hay suficiente stock de {producto.nombre}. Solo hay {producto.stock} kilos disponibles.")
                    return redirect('ventas')  # Redirige de vuelta a la página de ventas en caso de error
                producto.stock -= Decimal(ventas_producto.cantidad_producto)  # Resta la cantidad vendida del stock.
                producto.save()

                ventas_producto.save()
                messages.success(request, "Producto añadido a la venta.")
            else:
                messages.error(request, "Error al añadir producto.")

        elif action == 'checkout':
            venta_actual = Venta.objects.filter(abierta=True).first()
            productos_venta = ProductoVenta.objects.filter(venta=venta_actual) if venta_actual else []

            if venta_actual:
                    # Guardar el método de pago
                    if venta_form.is_valid():
                        venta_actual.metodo_de_pago = venta_form.cleaned_data['metodo_de_pago']
                        venta_actual.abierta = False
                        venta_actual.save()
                
                        ticket_url = generar_ticket_pdf(venta_actual, productos_venta)  # Generar el PDF y obtener la URL
                        messages.success(request, f"Venta finalizada. <a href='{ticket_url}' target='_blank'>Descargar Ticket</a>")  # Mensaje de éxito con enlace para descargar
                
                        return redirect('ventas')
                    else:
                        messages.error(request, "Error al finalizar la venta. Por favor, selecciona un método de pago.")
            return redirect('ventas')

    # Calculate the total sale amount
    total_venta = sum([pv.subtotal_producto for pv in productos_venta])

    return render(request, 'ventas.html', {
        'venta_form': venta_form, 
        'ventas_producto_form': ventas_producto_form, 
        'productos_venta': productos_venta,
        'total_venta': total_venta,
        'venta_actual': venta_actual,
        'productos_list': productos,

    })


def generar_ticket_pdf(venta, productos_venta):
    # Configurar el tamaño de la página para 58mm
    page_width = 58 / 25.4 * inch  # Convertir mm a pulgadas, luego a puntos
    page_height = 11 * inch  # La longitud es variable
    page_size = (page_width, page_height)

    # Crear un objeto BytesIO para guardar el PDF
    buffer = BytesIO()

    # Crear un objeto canvas para dibujar en el buffer con el tamaño de página ajustado
    p = canvas.Canvas(buffer, pagesize=page_size)

    # Margen izquierdo
    left_margin = 6  # 6 puntos es un pequeño margen pero visible en una impresora térmica

    # Dibuja el contenido del ticket con el margen izquierdo
    p.drawString(left_margin, page_height - 40, "Puebla")
    p.drawString(left_margin, page_height - 55, f"ID de Venta: {venta.id_venta}")
    p.drawString(left_margin, page_height - 70, f"Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(left_margin, page_height - 90, "Productos:")

    # Dibuja los productos ajustando el ancho
    y_position = page_height - 105
    for producto_venta in productos_venta:
        p.drawString(left_margin, y_position, f"{producto_venta.producto.nombre} - {producto_venta.cantidad_producto}kg - ${producto_venta.subtotal_producto}")
        y_position -= 15
    p.drawString(left_margin, y_position - 20, f"Total: ${venta.total}")

    # Finaliza el dibujo en el canvas
    p.showPage()
    p.save()

    # Mover el buffer al comienzo para leerlo
    buffer.seek(0)
    filename = f"ticket_{venta.id_venta}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, 'tickets', filename)
    directory = os.path.dirname(filepath)

    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, 'wb') as f:
        f.write(buffer.getvalue())
    
    # Asegurarse de cerrar el buffer
    buffer.close()

    # Devuelve la ruta al PDF
    return os.path.join(settings.MEDIA_URL, 'tickets', filename)


def add_product(request):
    if request.method == 'POST':
        form = VentasProductoForm(request.POST)
        if form.is_valid():
            ProductoVenta = form.save(commit=False)
        
            venta = Venta.objects.get_or_create(abierta=True, defaults={'total': 0})
            
            ProductoVenta.venta = venta
            ProductoVenta.subtotal_producto = ProductoVenta.cantidad_producto * ProductoVenta.producto.precio
            ProductoVenta.save()

            return redirect('ventas')  # Redirige al usuario a la página de ventas después de agregar el producto

    else:
        form = VentasProductoForm()  # Crea un formulario vacío si la solicitud es GET

    context = {
        'form': form
    }
    return render(request, 'ventas.html', context)

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == 'POST':
        form = AñadirProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('/inventario') 
    else:
        form = AñadirProductoForm(instance=producto)
    return render(request, '/inventario', {'form': form})

def editar_producto(request, producto_id):
    # Obtener el producto por su ID o retornar un error 404 si no se encuentra
    producto = get_object_or_404(Producto, id_producto=producto_id)

    # Si el método es POST, entonces estamos recibiendo datos para actualizar el producto
    if request.method == 'POST':
        form = AñadirProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('inventario')  # Suponiendo que 'inventario' es el nombre de la vista de inventario

    # Si el método es GET o cualquier otro, simplemente mostramos el formulario prellenado para el producto
    else:
        form = AñadirProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form})




def user_login(request):
    # Si el usuario ya está autenticado, redirígelo a ventas
    if request.user.is_authenticated:
        return redirect('ventas')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ventas')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'login.html')





def checkout (request):
    venta = Venta.objects.filter(abierta=True).first()
    

    if venta:
        venta.total = sum([pv.subtotal_producto for pv in venta.productoventa_set.all()])

        # Marca la venta como cerrada
        venta.abierta = False

        venta.save()

    return redirect(request,'ventas')

def add_suministro(request):
    if request.method == 'POST':
        form = Suministroform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/proveedores')
    else:
        form = Suministroform()
    return render(request, 'proveedores.html', {'form': form})

@login_required
def inventario(request,id_producto=None):
    
    productos_list = Producto.objects.all() 
    if id_producto is not None:
        producto = get_object_or_404(Producto, pk=id_producto)
        producto.delete()
        return redirect ('/inventario')
    

    if request.method == 'POST':
        form = AñadirProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('.')
    else:
        form = AñadirProductoForm()
    context = {'productos_list': productos_list, 'form': form}
    return render(request, 'inventario.html', context)

@login_required
def proveedores(request):
    Suministro_list = Suministro.objects.all()
    if request.method == 'POST':
        form = Suministroform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/proveedores')
    else:
        form = Suministroform()
    context = {'Suministro_list': Suministro_list, 'form': form}
    return render(request,'proveedores.html',context)




@login_required
def historial(request):
    current_date = timezone.now().date() 
    start_date = current_date
    end_date = current_date + timezone.timedelta(days=1)
    ventas_del_dia = Venta.objects.filter(fecha__range=(start_date, end_date))
    total_vendido = ventas_del_dia.aggregate(Sum('total'))['total__sum'] or 0
    total_efectivo = ventas_del_dia.filter(metodo_de_pago='efectivo').aggregate(Sum('total'))['total__sum'] or 0
    total_tarjeta = ventas_del_dia.filter(metodo_de_pago='tarjeta').aggregate(Sum('total'))['total__sum'] or 0
    total_transferencia = ventas_del_dia.filter(metodo_de_pago='transferencia').aggregate(Sum('total'))['total__sum'] or 0
    print("Total Efectivo:", total_efectivo)
    print("Total Tarjeta:", total_tarjeta)
    print("Total Transferencia:", total_transferencia)

    print (ventas_del_dia)
    productos_venta = []  # Lista para guardar los productos de la venta
    venta = None
    form = BuscarVentaForm(request.GET or None)
    
    if form.is_valid():
        try:
            venta_id = form.cleaned_data['id_venta']
            venta = Venta.objects.get(id_venta=venta_id)
            productos_venta = ProductoVenta.objects.filter(venta=venta)  # Obteniendo los productos de esa venta específica
        except Venta.DoesNotExist:
            messages.error(request, "Venta no encontrada.")
    
    context = {
        'productos_venta': productos_venta,
        'venta': venta,
        'form': form,
        'ventas_del_dia': ventas_del_dia,
    'total_vendido': total_vendido,
    'total_efectivo': total_efectivo,
    'total_tarjeta': total_tarjeta,
    'total_transferencia': total_transferencia,
    }
    
    
    return render(request, 'historial.html', context)

@login_required
def devoluciones(request):
    devoluciones_list = Devolucion.objects.all()

    for devolucion in devoluciones_list:
        # Obtener solo los productos que se devolvieron para esta devolución específica
        devolucion.productos_devueltos = ProductoVenta.objects.filter(devolucion=devolucion)

    ventas_list = Venta.objects.all()
    productos_list = Producto.objects.all()

    form = BuscarVentaForm(request.GET or None)
    if request.method == 'POST':
        form = BuscarVentaForm(request.POST)
        if form.is_valid():
            return redirect('/devoluciones')
        
    form = BuscarVentaForm()
    context = {
        'ventas_list': ventas_list, 
        'productos_list': productos_list, 
        'form': form, 
        'devoluciones_list': devoluciones_list
    }
    return render(request,'devoluciones.html', context)

def mapa (request):
    if request.method == 'POST':
        city_name = request.POST.get('city_name')
        api_key = 'TU_CLAVE_DE_API_OPENWEATHERMAP'  # Reemplaza con tu clave de API
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            context = {
                'city_name': city_name,
                'temperature': temperature,
                'weather_description': weather_description,
            }
            return render(request, 'weather/result.html', context)
        else:
            error_message = 'No se encontraron datos para la ciudad especificada.'
            return render(request, 'weather/search.html', {'error_message': error_message})

    return render(request, 'mapa.html')

@login_required
def home(request):
    return render (request,'home.html')

@login_required
def cuenta (request):
    return render (request,'cuenta.html')


    
def manage_account(request):
    registration_form = UserRegistrationForm()
    update_form = UserUpdateForm(instance=request.user if request.user.is_authenticated else None)
    password_change_form = PasswordChangeForm()
    
    if request.method == "POST":
        # Registro de usuario
        if 'register_submit' in request.POST:
            registration_form = UserRegistrationForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save(commit=False)
                user.set_password(registration_form.cleaned_data['password'])  # Hash the password
                user.save()
                messages.success(request, 'Usuario registrado exitosamente.')
                
        # Actualización de datos de usuario
        elif 'update_submit' in request.POST:
            update_form = UserUpdateForm(request.POST, instance=request.user)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'Datos actualizados exitosamente.')
            else:
                messages.error(request, f"Error: {update_form.errors}")

                
        # Cambio de contraseña
        elif 'password_change_submit' in request.POST:
            password_change_form = PasswordChangeForm(request.POST)
            if password_change_form.is_valid():
                current_password = password_change_form.cleaned_data['current_password']
                new_password = password_change_form.cleaned_data['new_password']
                confirm_password = password_change_form.cleaned_data['confirm_password']

                if not request.user.check_password(current_password):
                    messages.error(request, 'Contraseña actual incorrecta.')
                elif new_password != confirm_password:
                    messages.error(request, 'Las contraseñas no coinciden.')
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    logout(request)
                    messages.success(request, 'Contraseña cambiada exitosamente. Por favor, inicie sesión nuevamente.')
                    return redirect('login.html')
                    
    context = {
        'registration_form': registration_form,
        'update_form': update_form,
        'password_change_form': password_change_form
    }
    return render(request, 'cuenta.html', context)

def buscar_venta(request):
    venta = None
    productos_venta = []  # Lista para guardar los productos de la venta
    form = BuscarVentaForm(request.GET or None)
    if form.is_valid():
        try:
            venta_id = form.cleaned_data['id_venta']
            venta = Venta.objects.get(id_venta=venta_id)
            productos_venta = ProductoVenta.objects.filter(venta=venta)  # Obteniendo los productos de esa venta específica
        except Venta.DoesNotExist:
            messages.error(request, "Venta no encontrada.")
    context = {'form': form, 'venta': venta, 'productos_venta': productos_venta}
    return render(request, 'historial.html', context)

def buscar_ventas(request):
    venta = None
    productos_venta = []  
    form = BuscarVentaForm(request.GET or None)
    forms = DevolucionForm(request.GET or None)
    if form.is_valid():
        try:
            venta_id = form.cleaned_data['id_venta']
            venta = Venta.objects.get(id_venta=venta_id)
            productos_venta = ProductoVenta.objects.filter(venta=venta)  # Obteniendo los productos de esa venta específica
        except Venta.DoesNotExist:
            messages.error(request, "Venta no encontrada.")
    context = {'form': form, 'venta': venta, 'productos_venta': productos_venta, 'forms': forms}
    return render(request, 'devoluciones.html', context)


def procesar_devolucion(request, id_venta):
    venta = get_object_or_404(Venta, id_venta=id_venta)
    productos_venta = ProductoVenta.objects.filter(venta=venta)

    
    if request.method == 'POST':
        form = DevolucionForm(request.POST)
        if form.is_valid():
            # Iterar sobre los productos seleccionados
            for productoventa_id in request.POST.getlist('producto_a_devolver'):
                productoventa = ProductoVenta.objects.get(id=productoventa_id)
                Devolucion.objects.create(   # Aquí estamos usando el modelo Devolucion directamente
                    venta=venta,
                    producto=productoventa,
                    razon=form.cleaned_data['razon'],
                    comentarios=form.cleaned_data['comentarios']
                )
            messages.success(request, "Devolución procesada con éxito.")
            return redirect('devoluciones')
    else:
        form = DevolucionForm(initial={'venta': venta})
    return render(request, 'devoluciones', {'venta': venta, 'productos_venta': productos_venta, 'form': form})

def pedidos(request):
    return render (request,'pedidos.html')

#def añadir_producto (request):
    #venta_actual = Venta.objects.filter(abierta=True).first()
    #cuantity = request.POST ["txt-cantidad"]
   # name = request.POST ["txt-producto"]
   # Prod =  ProductoVenta.objects.create(Producto = name, cantidad_producto = cuantity, venta = venta_actual )

   # return redirect ("ventas/" )

def añadir_producto(request):
    if request.method == 'POST':
        datos_formulario = request.POST
        venta_actual = Venta.objects.filter(abierta=True).first()

        # Si no hay venta abierta, crear una nueva venta
        if not venta_actual:
            venta_actual = Venta.objects.create(abierta=True)

        # Obtiene el nombre del producto y la cantidad del formulario
        nombre_producto = datos_formulario['txt-producto']
        cantidad_producto = Decimal(datos_formulario['txt-cantidad'])

        # Crea un objeto ProductoVenta y lo asocia con el producto y la venta actual
        producto_venta = ProductoVenta(
            producto=Producto.objects.get(nombre=nombre_producto),
            cantidad_producto=cantidad_producto,
            venta=venta_actual,
        )

        # Guarda el objeto ProductoVenta en la base de datos
        producto_venta.save()
        return redirect('ventas')

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from decimal import Decimal
from .models import Producto, ProductoVenta, Venta
from django.db.models import Q
from django.contrib import messages

def procesar_codigo_barras(request):
    if request.method == 'POST':
        codigo_barras = request.POST.get('codigo_barras')
        id_producto = int(codigo_barras[:6])
        peso = Decimal(int(codigo_barras[6:11])) / 100  # Convertir a kilogramos
        producto = get_object_or_404(Producto, pk=id_producto)

        # Comprobar si existe una venta abierta
        venta_actual = Venta.objects.filter(abierta=True).first()
        if not venta_actual:
            # Si no hay venta abierta, crear una nueva
            venta_actual = Venta.objects.create(abierta=True)

        if producto.stock < peso:
            messages.error(request, f"No hay suficiente stock de {producto.nombre}. Solo hay {producto.stock} kilos disponibles.")
            return redirect('ventas')

        # Crear y guardar el ProductoVenta
        producto_venta = ProductoVenta(producto=producto, cantidad_producto=peso, venta=venta_actual)
        producto_venta.save()

        # Actualizar el stock del producto
        producto.stock -= peso
        producto.save()

        messages.success(request, "Producto añadido correctamente a la venta.")
        return redirect('ventas')
    else:
        messages.error(request, "Solicitud inválida.")
        return redirect('ventas')


