import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models.ingresos_model import Transaccion
from models.vehiculo_models import Vehiculo
from views import header_view

header_bp = Blueprint('header', __name__)

# Ruta principal
@header_bp.route("/")
def get_home():
    vehiculos = Vehiculo.ver_vehiculos_dest()  # Obtén los vehículos
    return header_view.home(vehiculos=vehiculos)  # Pasa los vehículos a la vista

# Ruta de contacto
@header_bp.route('/contacto')
def get_contacto():
    return header_view.contacto()

# Ruta de contacto
@header_bp.route('/sobre')
def get_sobreNosotros():
    return header_view.sobreNostros()

# Ruta de inventario
@header_bp.route('/inventario')
def get_inventario():
    vehiculos = Vehiculo.ver_inventario()  # Obtén los vehículos
    return header_view.inventario(vehiculos=vehiculos)  # Pasa los vehículos a la vista

@header_bp.route('/financiamiento')
def get_financiamiento():
    return header_view.financiamiento()  # Pasa los vehículos a la vista

@header_bp.route('/servicios')
def get_servicios():
    return header_view.servicios()  # Pasa los vehículos a la vista

@header_bp.route('/servicios/alquileres')
def get_alquiler():
    return header_view.alquileres()  # Pasa los vehículos a la vista

@header_bp.route('/inventario/detalle')
def get_detalle():
    return header_view.detalleVehiculo()  # Pasa los vehículos a la vista

@header_bp.route('/inventario', methods=["GET", "POST"])
def get_filtro():
    if request.method == "POST":
        tipo_servicio = request.form.get("tipo_vehiculo")
        marca = request.form.get("marca")
        precio = request.form.get("precio")
        anio = request.form.get("anio")
        kilometraje = request.form.get("kilometraje")
        combustible = request.form.get("combustible")

        # Procesar rango de precios
        precio_min, precio_max = None, None
        if precio:
            rango_precio = precio.split(" - ")
            if len(rango_precio) == 2:
                try:
                    precio_min = float(rango_precio[0].replace('$', '').replace(',', '').strip())
                    precio_max = float(rango_precio[1].replace('$', '').replace(',', '').strip())
                except ValueError:
                    precio_min = precio_max = None

        # Procesar kilometraje
        if kilometraje:
            try:
                kilometraje = int(kilometraje.replace(' km', '').replace(',', '').strip())
            except ValueError:
                kilometraje = None

        # Filtrar vehículos según tipo de servicio
        if tipo_servicio == "Venta":
            vehiculos = Vehiculo.filtrar_por_venta(
                marca=marca,
                precio_min=precio_min,
                precio_max=precio_max,
                anio=anio,
                combustible=combustible
            )
        elif tipo_servicio == "Alquiler":
            vehiculos = Vehiculo.filtrar_por_alquiler(
                marca=marca,
                precio_min=precio_min,
                precio_max=precio_max,
                anio=anio,
                kilometraje=kilometraje,
                combustible=combustible
            )
        else:
            # Si no se selecciona tipo_servicio, filtrar considerando ambos tipos
            vehiculos = Vehiculo.filtrar_vehiculos(
                marca=marca,
                precio_min=precio_min,
                precio_max=precio_max,
                anio=anio,
                kilometraje=kilometraje,
                combustible=combustible
            )

    else:
        vehiculos = Vehiculo.ver_vehiculos()  # Todos los vehículos si no hay filtros

    return header_view.filtro(vehiculos=vehiculos)

@header_bp.route('/inventario/vehicle/<int:id_vehiculo>')
def get_detalles_vehiculo(id_vehiculo):
    print(f"ID recibido: {id_vehiculo}")
    list_vehiculo = Vehiculo.detail(id_vehiculo)
    
    if not list_vehiculo:
        flash("El vehículo no existe.", "error")
        return redirect(url_for('header.get_inventario'))
    
    vehiculo = list_vehiculo[0]
    estado_vehiculo = list_vehiculo[1]
    marca = list_vehiculo[2]

    print(f"Vehículo encontrado: {vehiculo}")
    return render_template(
        'detalles_vehiculo.html',
        vehiculo=vehiculo,
        estado_vehiculo=estado_vehiculo,
        marca=marca
    )

@header_bp.route('/inventario/vehicle/<int:id_vehiculo>/compra', methods=['GET', 'POST'])
def formulario_compra(id_vehiculo):
    # Verificar si el usuario ha iniciado sesión
    if 'user' not in session:
        flash("Debes iniciar sesión para realizar una compra.", "warning")
        session['next_url'] = url_for('header.formulario_compra', id_vehiculo=id_vehiculo)
        return redirect(url_for('auth.login'))  # Redirigir al formulario de inicio de sesión

    if request.method == 'POST':
        # Captura los datos del formulario
        id_cliente = session.get('cliente_id')
        fecha = datetime.datetime.now().date()
        monto = request.form.get('monto')

        # Procesar la compra
        resultado = Transaccion.procesar_compra(id_cliente, id_vehiculo, monto, fecha)

        if resultado['success']:
            flash(resultado['message'], "success")
            return redirect(url_for('header.get_inventario'))
        else:
            flash(resultado['message'], "error")
            return redirect(url_for('header.get_inventario'))

    # Obtener detalles del vehículo para mostrar en el formulario
    vehicle = Vehiculo.find_by(id_vehiculo)
    if not vehicle:
        flash("El vehículo no existe.", "error")
        return redirect(url_for('header.get_inventario'))

    return render_template('servicios/formulario_compra.html', vehicle=vehicle)

@header_bp.route('/inventario/vehicle/<int:id_vehiculo>/alquiler', methods=['GET', 'POST'])
def formulario_alquiler(id_vehiculo):
    # Verificar si el usuario ha iniciado sesión
    if 'user' not in session:
        flash("Debes iniciar sesión para alquilar un auto.", "warning")
        session['next_url'] = url_for('header.formulario_alquiler', id_vehiculo=id_vehiculo)
        return redirect(url_for('auth.login'))  # Redirigir al formulario de inicio de sesión

    if request.method == 'POST':
        # Captura los datos del formulario
        id_cliente = session.get('cliente_id')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        fecha_transaccion =  datetime.datetime.now().date()
        costo_total = request.form.get('costo_total')

        # Procesar el alquiler
        resultado = Transaccion.procesar_alquiler(id_cliente, id_vehiculo, fecha_inicio, fecha_fin, costo_total, fecha_transaccion)

        if resultado['success']:
            flash(resultado['message'], "success")
            return redirect(url_for('header.get_inventario'))
        else:
            flash(resultado['message'], "error")
            return redirect(url_for('header.get_inventario'))

    # Obtener detalles del vehículo para mostrar en el formulario
    vehicle = Vehiculo.find_by(id_vehiculo)
    if not vehicle:
        flash("El vehículo no existe.", "error")
        return redirect(url_for('header.get_inventario'))

    return render_template('servicios/formulario_alquiler.html', vehicle=vehicle)
