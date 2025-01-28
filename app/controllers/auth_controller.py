from datetime import datetime
from database import db 
from flask import Blueprint, request, redirect, session, url_for, flash, render_template
from config import index_dat, prepair_list
from models.vehiculo_models import Vehiculo
from models.empleado_models import EmpleadoPersona
from models.cliente_models import ClientePersona
from models.reporte_models import Reporte
from models.seguro_models import Seguro
from models.vehiculo_models import Vehiculo
from models.aseguradora_models import Aseguradora
from models.user_models import User
from models.persona_models import Persona
from models.ingresos_model import TipoCambio, Transaccion
import calendar

from views import auth_view

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return auth_view.login_view()  # Llama a la vista de inicio de sesión
    try:
        username = request.form['username']
        password = request.form['password']

        # Validar el usuario
        user = User.validate_user(username, password)
        if user["success"]:
            # Almacenar el nombre completo y rol en la sesión
            session['cliente_id'] = user["cliente_id"]  
            session['empleado_id'] = user["empleado_id"]  
            session['user'] = username
            session['user_fullname'] = user["fullname"]  # Suponiendo que el modelo devuelve el nombre completo
            session['role'] = user["role"]  # Suponiendo que el modelo devuelve el rol del usuario

            print(f"Inicio de sesión exitoso: {session['user_fullname']} ({session['role']})")

             # Redirigir al URL original si existe
            next_url = session.pop('next_url', None)  # Elimina `next_url` después de usarlo
            if next_url:
                return redirect(next_url)
            
            # Redirigir según el rol del usuario
            if session['role'] == 'Admin':  # Admin es un Empleado
                return redirect(url_for('auth.admin_dashboard'))
            elif session['role'] == 'User':  # User es un Cliente
                return redirect(url_for('header.get_home'))
            else:
                flash("Rol no válido. No tienes permisos para acceder a esta área.", "error")
                return redirect(url_for('auth.login'))  # Regresar al login si el rol es inválido
        else:
            flash(user["message"], "error")
            print("Error en las credenciales")
    except Exception as ex:
        flash('Ocurrió un error al intentar iniciar sesión.', 'error')
        print(f"Error al intentar iniciar sesión: {ex}")

    return auth_view.login_view()  # Volver al formulario de inicio de sesión


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for('auth.login'))  # Redirige al formulario de inicio de sesión


@auth_bp.route('/admin-dashboard')
def admin_dashboard():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado

    connection = db()  # Conexión a la base de datos
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Vehículos en Inventario
            cursor.execute("SELECT COUNT(*) AS total_vehiculos FROM VEHICULO WHERE idEstadoVehiculo = 1;")
            vehiculos_inventario = cursor.fetchone()['total_vehiculos']

            # Ventas del Mes
            cursor.execute("""
                SELECT COUNT(*) AS ventas_mes 
                FROM TRANSACCION 
                WHERE tipoTransaccion = 'Venta' 
                AND MONTH(fechaTransaccion) = MONTH(CURRENT_DATE()) 
                AND YEAR(fechaTransaccion) = YEAR(CURRENT_DATE());
            """)
            ventas_mes = cursor.fetchone()['ventas_mes']

            # Alquileres Activos
            cursor.execute("""
                SELECT COUNT(*) AS alquileres_activos 
                FROM RESERVA 
                WHERE fechaFin >= CURRENT_DATE() AND fechaInicio <= CURRENT_DATE();
            """)
            alquileres_activos = cursor.fetchone()['alquileres_activos']

        return render_template(
            'admin/admin_dashboard.html',
            vehiculos_inventario=vehiculos_inventario,
            ventas_mes=ventas_mes,
            alquileres_activos=alquileres_activos
        )
    except Exception as e:
        print(f"Error al cargar el dashboard: {e}")
        flash("Error al cargar el dashboard. Intenta nuevamente más tarde.", "error")
        return redirect(url_for('auth.login'))
    finally:
        connection.close()

#VEHICULOS
@auth_bp.route('/admin-dashboard/vehiculo/gestion-vehiculos')
def admin_gestion_vehiculos():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    vehiculos = Vehiculo.find_all()
    return auth_view.gestion_vehiculos_view(vehiculos=vehiculos)  # Llama a la vista del panel de administración

@auth_bp.route('/admin-dashboard/vehiculo/agregar-vehiculo',methods=["GET","POST"])
def admin_creacion_vehiculos():
      if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
      if(request.method == "GET"):
            return auth_view.creacion_vehiculos_view()
      try:
            id_vehiculo = request.form['idVehiculo']
            anio = request.form['anio']
            modelo = request.form['modelo']
            precio_diario = request.form['precioDiario']
            precio_dolar = request.form['precioDolar']
            caracteristicas = request.form['caracteristicas']
            id_estado_vehiculo = request.form['idEstadoVehiculo']
            id_marca = request.form['idMarca']      

            vehiculo = Vehiculo(id_vehiculo,anio,modelo,precio_diario,precio_dolar,caracteristicas,id_estado_vehiculo,id_marca)
            if vehiculo.create() is not None:
                  flash(f'Se registro correctamente, vehiculo: {id_vehiculo} ','success')
            else:
                  flash('Ocurrio un error al registrar','error')
      except Exception as ex:
            flash('No se pudo registrar, error','error')
      return  redirect(url_for('auth.admin_gestion_vehiculos'))

@auth_bp.route('/admin-dashboard/<int:id>')
def admin_get_vehiculo(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado  
    list_vehiculo = Vehiculo.detail(id)
    return auth_view.get_vehiculo_view(vehiculo=list_vehiculo[0],estado_vehiculo=list_vehiculo[1],marca=list_vehiculo[2])

@auth_bp.route('/admin-dashboard/vehiculo/<int:id>/edit',methods=["POST","GET"])
def admin_edit_vehiculo(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    
    vehiculo = Vehiculo.find_by(id)
    vehiculo.to_string()
      
    if request.method == "GET":
        return auth_view.edit_view(vehiculo=vehiculo)
    anio = request.form['anio']
    modelo = request.form['modelo']
    precio_diario = request.form['precio_diario']
    precio_dolar = request.form['precio_dolar']
    caracteristicas = request.form['caracteristicas']
    imagen_url = request.form['imagen_url']
    combustible = request.form['combustible']
    kilometraje = request.form['kilometraje']
    vehiculo.to_string()

    vehiculo.update(anio=anio,modelo=modelo,precio_diario=precio_diario,precio_dolar=precio_dolar,caracteristicas=caracteristicas,imagen_url=imagen_url,combustible=combustible,kilometraje=kilometraje)
    flash(f"Se actualizo correctamente el vehiculo: {id}",'success')
    return redirect(url_for('auth.admin_gestion_vehiculos'))

@auth_bp.route("/admin-dashboard/vehiculo/<int:id>/delete")
def admin_delete_vehiculo(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    vehiculo = Vehiculo.delete(id_vehiculo=id)
    flash(f'Se elimino el vehiculo correctamente: {id}','error')
    return redirect(url_for('auth.admin_gestion_vehiculos'))

#------------- buscar
def admin_perfom_search(index,query):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    query = query.lower().strip()
    results = set()

    if query in index:
        results.update(index[query])
    else:
        query_words = query.split()
        for word in query_words:
            if word in index:
                results.update(index[word])
    return list(results)

#metodos de casos de uso
@auth_bp.route("/admin-dashboard/vehiculo/results",methods=["GET"])
def admin_buscar_vehiculo():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    list_data = prepair_list()
    index_end = index_dat(list_data)
    query = request.args.get('query')
    list_results = admin_perfom_search(index=index_end,query=query)
    results = []
    for key in list_results:
        vehiculo =  Vehiculo.find_by(key)
        results.append({
            "id_vehiculo":vehiculo.id_vehiculo,
            "id_estado_vehiculo":vehiculo.id_estado_vehiculo,
            "id_marca":vehiculo.id_marca,
            "año":vehiculo.anio,
            "modelo":vehiculo.modelo,
            "precio_diario":vehiculo.precio_diario,
            "precio_dolar":vehiculo.precio_dolar,
            "caracteristicas":vehiculo.caracteristicas
        })
    return auth_view.gestion_vehiculos_view(vehiculos=results)

# seguimiento vehiculo
@auth_bp.route("/admin-dashboard/vehiculo/seguimiento")
def admin_seguimiento_vehiculo():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    segui = Vehiculo.seguimient()
    return auth_view.seguimiento_view(seg=segui)

#EMPLEADOS
@auth_bp.route('/admin-dashboard/empleado/create', methods=['GET', 'POST'])
def admin_create_empleado():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == 'GET':
        return auth_view.create_empleado_view()
    # Validación de datos
    required_fields = ['nom_empleado', 'ap_paterno_empleado', 'ap_materno_empleado', 'direccion', 'telefono', 'fecha_nac', 'email', 'ci', 'usuario', 'password', 'rol']
    for field in required_fields:
        if field not in request.form or not request.form[field]:
            flash(f'El campo {field.replace("_", " ")} es obligatorio.', 'error')
            return redirect(url_for('auth.admin_create_empleado'))
    # Procesar datos
    try:
        nombre = request.form['nom_empleado']
        ap_paterno = request.form['ap_paterno_empleado']
        ap_materno = request.form['ap_materno_empleado']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        fecha_nac = datetime.strptime(request.form['fecha_nac'], '%Y-%m-%d').date()
        email = request.form['email']
        ci = request.form['ci']
        usuario = request.form['usuario']
        contraseña = request.form['password']
        rolusuario = request.form['rol']

        id_persona = EmpleadoPersona.create_persona(nombre, ap_paterno, ap_materno, direccion, telefono, email, fecha_nac)
        id_empleado = EmpleadoPersona.create_empleado(id_persona, email, ci, "0%")
        EmpleadoPersona.create_usuario(id_empleado, usuario, contraseña, rolusuario)
        
        flash("Empleado creado con éxito", "success")
        return redirect(url_for('auth.admin_empleados'))
    except Exception as ex:
        flash('Ocurrió un error al crear el empleado: ' + str(ex), 'error')
        return redirect(url_for('auth.admin_create_empleado'))

@auth_bp.route('/admin-dashboard/empleados', methods=['GET', 'POST'])
def admin_empleados():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    search_query = request.args.get('buscar', '')
    empleados = EmpleadoPersona.search_by_name(search_query) if search_query else EmpleadoPersona.find_all()
    return auth_view.gestion_empleados_view(empleados)

@auth_bp.route('/admin-dashboard/empleados/<int:id>')
def admin_empleado(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    empleado = EmpleadoPersona.find_by(id)
    if empleado is None:
        flash('No hay un empleado con ese ID.', 'error')
        return redirect(url_for('auth.admin_empleados'))
    return auth_view.empleado_view(empleado=empleado)

@auth_bp.route('/admin-dashboard/empleados/<int:id>/update', methods=["GET", "POST"])
def admin_update_empleado(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == "GET":
        empleado = EmpleadoPersona.find_by_empleado(id)
        if empleado is None:
            flash('No hay un empleado con ese ID.', 'error')
            return redirect(url_for('auth.admin_empleados'))
        return auth_view.update_empleado_view(empleado=empleado)
    
    # Validación de datos
    email_nuevo = request.form.get('email')
    ci_nuevo = request.form.get('ci')
    comisionES_nueva = request.form['comisionES']
    if not email_nuevo or not ci_nuevo:
        flash('Email y CI son obligatorios.', 'error')
        return redirect(url_for('auth.admin_update_empleado', id=id))

    EmpleadoPersona.update_empleado(id_empleado=id, email=email_nuevo, ci=ci_nuevo,comisionES=comisionES_nueva)
    flash("Empleado actualizado correctamente", "success")
    return redirect(url_for('auth.admin_empleados'))

@auth_bp.route('/admin-dashboard/empleados/<int:id>/delete')
def admin_delete_empleado(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    EmpleadoPersona.delete_empleado(id)
    flash("Empleado eliminado correctamente", "success")
    return redirect(url_for('auth.admin_empleados'))


#REPORTE
@auth_bp.route('/admin-dashboard/reporte/reporte_1')
def reporte_1():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    reporte = Reporte.reporte_1()
    return auth_view.reporte_1_view(reporte)

@auth_bp.route('/admin-dashboard/reporte/reporte_2')
def reporte_2():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    reporte = Reporte.reporte_2()
    return auth_view.reporte_2_view(reporte)

@auth_bp.route('/admin-dashboard/reporte/reporte_3')
def reporte_3():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    reporte = Reporte.reporte_3()
    return auth_view.reporte_3_view(reporte)

@auth_bp.route('/admin-dashboard/reporte/reporte_4')
def reporte_4():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    reporte = Reporte.reporte_4()
    return auth_view.reporte_4_view(reporte)

@auth_bp.route('/admin-dashboard/reporte/reporte_5')
def reporte_5():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    reporte = Reporte.reporte_5()
    return auth_view.reporte_5_view(reporte)

#SEGUROS

@auth_bp.route('/admin-dashboard/seg')
def admin_seguros():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    seguros = Seguro.find_all()
    return auth_view.seguros_view(seguros)

@auth_bp.route('/admin-dashboard/seg/create/seguro', methods=['GET', 'POST'])
def admin_create_seguro():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == 'GET':
        vehiculos = Vehiculo.find_all_ids()
        aseguradoras = Aseguradora.find_all_ids()
        return auth_view.create_seguro_view(vehiculos, aseguradoras)
    
    id_seguro = request.form['id_seguro']
    id_vehiculo = request.form['id_vehiculo']
    id_aseguradora = request.form['id_aseguradora']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    tipo_seguro = request.form['tipo_seguro']
    costo = request.form['costo']
      
    fecha_inicio_str = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin_str = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    Seguro.create_seguro(id_seguro, id_vehiculo, id_aseguradora, fecha_inicio_str, fecha_fin_str, tipo_seguro, costo)

    return redirect(url_for('auth.admin_seguros'))


@auth_bp.route('/admin-dashboard/seg/update/<int:id>', methods=["GET", "POST"])
def admin_update(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == "GET":
        seguro = Seguro.find_by(id)
        vehiculos = Vehiculo.find_all_ids()
        aseguradoras = Aseguradora.find_all_ids()
        if seguro is None:
            return redirect(url_for('auth.admin_seguros'))
        return auth_view.update_seguro_view(seguro=seguro, vehiculos=vehiculos, aseguradoras=aseguradoras)
    
    # Recoleccion de la informacion
    id_vehiculo = request.form['id_vehiculo']
    id_aseguradora = request.form['id_aseguradora']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    tipo_seguro = request.form['tipo_seguro']
    costo = request.form['costo']

    fecha_inicio_str = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin_str = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    # Update del seguro
    Seguro.update_seguro(id, id_vehiculo, id_aseguradora, fecha_inicio_str, fecha_fin_str, tipo_seguro, costo)
    flash('Seguro actualizado exitosamente!', 'success')
    return redirect(url_for('auth.admin_seguros'))

@auth_bp.route('/admin-dashboard/seg/delete/<int:id>')
def admin_delete_seguro(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    seguro = Seguro.find_by(id)
    if seguro is None:
        flash('No existe un seguro con ese id', 'error')
    else:
        Seguro.delete_seguro(id)
    return redirect(url_for('auth.admin_seguros'))

@auth_bp.route('/admin-dashboard/seg/<int:id>')
def admin_buscar_seguro(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    seguro = Seguro.find_by(id)
    if seguro is None:
        return redirect(url_for('auth.admin_seguros'))
    return auth_view.seguro_view(seguro=seguro)

@auth_bp.route('/admin-dashboard/rep/vencidos', methods=['GET'])
def admin_seg_vencido():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    seguros = Seguro.seguros_vencidos()
    return auth_view.seguros_vencidos_view(seguros)

@auth_bp.route('/admin-dashboard/rep/activos', methods=['GET'])
def admin_seg_activo():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    seguros = Seguro.seguros_activos()
    return auth_view.seguros_activos_view(seguros)

#ASEGURADORA

@auth_bp.route('/admin-dashboard/aseg')
def admin_aseguradoras():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    aseguradoras = Aseguradora.find_all()
    return auth_view.aseguradoras_view(aseguradoras)

@auth_bp.route('/admin-dashboard/aseg/create/aseguradora', methods=['GET', 'POST'])
def admin_create_aseguradora():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == 'GET':
        return auth_view.create_aseguradora_view()
    id_aseguradora = request.form['id_aseguradora']
    nombre_aseguradora = request.form['nombre_aseguradora']
    contacto_aseguradora = request.form['contacto_aseguradora']

    Aseguradora.create_aseguradora(id_aseguradora, nombre_aseguradora, contacto_aseguradora)
    return redirect(url_for('auth.admin_aseguradoras'))

@auth_bp.route('/admin-dashboard/aseg/update/<int:id>', methods=["GET", "POST"])
def admin_update_aseguradora(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == "GET":
        aseguradora = Aseguradora.find_by(id)
        if aseguradora is None:
            return "No existe una aseguradora con ese id"
        return auth_view.update_aseguradora_view(aseguradora=aseguradora)
    id_aseguradora = request.form['id_aseguradora']
    nombre_aseguradora = request.form['nombre_aseguradora']
    contacto_aseguradora = request.form['contacto_aseguradora']

    Aseguradora.update_aseguradora(id_aseguradora, nombre_aseguradora, contacto_aseguradora)
    return redirect(url_for('auth.admin_aseguradoras'))

@auth_bp.route('/admin-dashboard/aseg/delete/<int:id>')
def admin_delete_aseguradora(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    Aseguradora.delete_aseguradora(id)
    return redirect(url_for('auth.admin_aseguradoras'))

@auth_bp.route('/admin-dashboard/aseg/<int:id>')
def admin_aseguradora(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    aseguradora = Aseguradora.find_by(id)
    if aseguradora is None:
        return "No existe una aseguradora con ese id"
    return auth_view.aseguradora_view(aseguradora=aseguradora)

@auth_bp.route('/admin-dashboard/rep')
def admin_aseguradora_rep():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    aseguradoras = Aseguradora.find_all()
    return auth_view.aseguradoras_reporte_view(aseguradoras)

"""#CLIENTES

# Ruta principal que muestra la lista de personas
@auth_bp.route('/admin-dashboard/clientes', methods=['GET'])
def get_personas():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    personas = Persona.get_all()
    return auth_view.clientes_view(personas)

# Ruta para mostrar el formulario de agregar persona
@auth_bp.route('/admin-dashboard/cliente/add', methods=['GET'])
def create_persona_form():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    return auth_view.create_cliente_view()

# Ruta para procesar el formulario de añadir persona
@auth_bp.route('/admin-dashboard/cliente/add', methods=['POST'])
def create_add_persona():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    nombre = request.form.get('nombre')
    paterno = request.form.get('paterno')
    materno = request.form.get('materno')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()

    nueva_persona = Persona(
        nombre=nombre,
        paterno=paterno,
        materno=materno,
        direccion=direccion,
        telefono=telefono,
        email=email,
        fecha_nacimiento=fecha_nacimiento
    )
    nueva_persona.save()
    return redirect(url_for('auth.get_personas'))

# Ruta para mostrar el formulario de edición con datos de una persona
@auth_bp.route('/admin-dashboard/cliente/edit/<int:id>', methods=['GET'])
def edit_persona_form(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    persona_obj = Persona.get_by_id(id)
    return auth_view.update_cliente_view(cliente=persona_obj)

# Ruta para procesar el formulario de edición de persona
@auth_bp.route('/admin-dashboard/cliente/edit/<int:id>', methods=['POST'])
def edit_persona(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    persona_obj = Persona.get_by_id(id)
    persona_obj.nombre = request.form.get('nombre')
    persona_obj.paterno = request.form.get('paterno')
    persona_obj.materno = request.form.get('materno')
    persona_obj.direccion = request.form.get('direccion')
    persona_obj.telefono = request.form.get('telefono')
    persona_obj.email = request.form.get('email')
    persona_obj.fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
    persona_obj.update()
    return redirect(url_for('auth.get_personas'))

# Ruta para eliminar una persona
@auth_bp.route('/admin-dashboard/cliente/delete/<int:id>', methods=['GET'])
def delete_persona(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    persona_obj = Persona.get_by_id(id)
    if persona_obj:
        persona_obj.delete()
    return redirect(url_for('auth.get_personas'))

# Ruta para descargar la información de una persona
@auth_bp.route('/admin-dashboard/cliente/download/<int:id>', methods=['GET'])
def download_persona(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    persona = Persona.get_by_id(id)
    if persona:
        return auth_view.cliente_download_view(persona)
    return redirect(url_for('auth.get_personas'))"""

# CLIENTES

# Ruta principal que muestra la lista de clientes
@auth_bp.route('/admin-dashboard/clientes', methods=['GET'])
def get_clientes():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    clientes = ClientePersona.find_all()
    return auth_view.clientes_view(clientes)

# Ruta para mostrar el formulario de agregar cliente
@auth_bp.route('/admin-dashboard/cliente/add', methods=['GET'])
def create_cliente_form():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    return auth_view.create_cliente_view()

# Ruta para procesar el formulario de añadir cliente
@auth_bp.route('/admin-dashboard/cliente/add', methods=['POST'])
def create_cliente():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado

    # Capturar datos del formulario
    nombre = request.form.get('nombre')
    paterno = request.form.get('paterno')
    materno = request.form.get('materno')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
    fecha_registro = datetime.now().strftime('%Y-%m-%d')  # Registrar la fecha actual

    # Crear la persona y el cliente asociado
    id_persona = ClientePersona.create_persona(nombre, paterno, materno, direccion, telefono, email, fecha_nacimiento)
    if id_persona:
        id_cliente = ClientePersona.create_cliente(id_persona, fecha_registro)
        if id_cliente:
            # Crear usuario asociado al cliente
            nombre_usuario = request.form.get('nombreUsuario')
            contrasena = request.form.get('contrasena')
            ClientePersona.create_usuario(id_cliente, nombre_usuario, contrasena)
            flash("Cliente creado exitosamente.", "success")
        else:
            flash("Error al crear cliente.", "danger")
    else:
        flash("Error al crear persona.", "danger")

    return redirect(url_for('auth.get_clientes'))

# Ruta para mostrar el formulario de edición de cliente
@auth_bp.route('/admin-dashboard/cliente/edit/<int:id>', methods=['GET'])
def edit_cliente_form(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    cliente = ClientePersona.find_by_id(id)
    return auth_view.update_cliente_view(cliente=cliente)

# Ruta para procesar el formulario de edición de cliente
@auth_bp.route('/admin-dashboard/cliente/edit/<int:id>', methods=['POST'])
def edit_cliente(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    cliente = ClientePersona.find_by_id(id)
    if cliente:
        cliente['nombre'] = request.form.get('nombre')
        cliente['paterno'] = request.form.get('paterno')
        cliente['materno'] = request.form.get('materno')
        cliente['direccion'] = request.form.get('direccion')
        cliente['telefono'] = request.form.get('telefono')
        cliente['email'] = request.form.get('email')
        cliente['fecha_nacimiento'] = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
        cliente['fecha_registro'] = datetime.strptime(request.form['fecha_registro'], '%Y-%m-%d').date()
        ClientePersona.update_cliente(
            cliente['idCliente'], 
            cliente['nombre'], 
            cliente['paterno'],
            cliente['materno'], 
            cliente['direccion'],
            cliente['telefono'],
            cliente['email'],
            cliente['fecha_nacimiento'],
            cliente['fecha_registro']
        )
        flash("Cliente actualizado exitosamente.", "success")
    else:
        flash("Cliente no encontrado.", "danger")

    return redirect(url_for('auth.get_clientes'))

# Ruta para eliminar un cliente
@auth_bp.route('/admin-dashboard/cliente/delete/<int:id>', methods=['GET'])
def delete_cliente(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    ClientePersona.delete_cliente(id)
    flash("Cliente eliminado exitosamente.", "success")
    return redirect(url_for('auth.get_clientes'))

# Ruta para descargar la información de un cliente
@auth_bp.route('/admin-dashboard/cliente/download/<int:id>', methods=['GET'])
def download_cliente(id):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    cliente = ClientePersona.find_by_id(id)
    if cliente:
        return auth_view.cliente_download_view(cliente)
    flash("Cliente no encontrado.", "danger")
    return redirect(url_for('auth.get_clientes'))


#INGRESOS

@auth_bp.route("/admin-dashboard/ingresos")
def admin_ingresos():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    transacciones = Transaccion.find_all()
    return render_template('admin/ingresos/ingresos.html', transacciones=transacciones)

def ingresos_men():
    meses = []
    costo = []
    datas = Transaccion.query("""
        SELECT DATE_FORMAT(fechatransaccion, '%Y-%m') AS mes, 
               SUM(costo) AS ingresos_mensuales
        FROM transaccion
        GROUP BY DATE_FORMAT(fechatransaccion, '%Y-%m')
        ORDER BY mes
    """)
    for data in datas:
        mes = int(data[0][-2:])
        meses.append(calendar.month_name[mes])
        costo.append(data[1])
    return [meses, costo]

def ingresos_tipo():
    tipo = []
    monto = []
    datas = Transaccion.query("""
        SELECT tipotransaccion, 
               COUNT(DISTINCT idcliente) AS cantidad_clientes
        FROM transaccion
        GROUP BY tipotransaccion
    """)
    for data in datas:
        tipo.append(data[0])
        monto.append(data[1])
    return [tipo, monto]

@auth_bp.route("/admin-dashboard/dashboard_ingresos")
def dashboard_ingresos():
    tipo_cambio_actual = TipoCambio.query("""
        SELECT valordolar 
        FROM tipo_cambio 
        ORDER BY fechatipocambio DESC 
        LIMIT 1
    """)
    cliente_activos = TipoCambio.query("SELECT COUNT(DISTINCT idcliente) FROM transaccion")
    total_transacciones = Transaccion.query("SELECT COUNT(*) FROM transaccion")
    ingresos = Transaccion.query("""
        SELECT SUM(costo) AS total_ingresos
        FROM transaccion
        WHERE fechatransaccion BETWEEN DATE_SUB(NOW(), INTERVAL 5 MONTH) AND NOW()
    """)
    dash_header = {
        "tipo_cambio": tipo_cambio_actual[0][0] if tipo_cambio_actual else None,
        "cliente_activos": cliente_activos[0][0] if cliente_activos else 0,
        "total_transacciones": total_transacciones[0][0] if total_transacciones else 0,
        "ingresos_total": ingresos[0][0] if ingresos else 0
    }

    ingresos_mensuales = ingresos_men()
    ingr_tipo = ingresos_tipo()
    return render_template("admin/ingresos/dashboard.html", header=dash_header, meses=ingresos_mensuales, tipo=ingr_tipo)

@auth_bp.route("/admin-dashboard/tipocambio/register", methods=["POST"])
def tipo_cambio_registrar():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    fecha_str = request.form["fechaTipoCambio"]
    valor_dolar = request.form["valorDolar"]
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")

    tipo_cambio = TipoCambio(fecha_tipo_cambio=fecha, valor_dolar=valor_dolar)
    if tipo_cambio.create():
        flash("Se registró correctamente", "success")
    else:
        flash("No se pudo registrar", "error")
    return redirect(url_for("auth.admin_ingresos"))

@auth_bp.route("/admin-dashboard/transacciones/register", methods=["POST"])
def transaccion_register():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    id_cliente = request.form["idCliente"]
    tipo_transaccion = request.form["tipoTransaccion"]
    fecha_transaccion_str = request.form["fechaTransaccion"]
    costo = request.form["costo"]
    id_tipo_cambio = request.form["idTipoCambio"]

    transaccion = Transaccion(
        id_cliente=id_cliente,
        tipo_transaccion=tipo_transaccion,
        fecha_transaccion=datetime.strptime(fecha_transaccion_str, "%Y-%m-%d"),
        costo=costo,
        id_tipo_cambio=id_tipo_cambio
    )
    if transaccion.create():
        flash("Se registró correctamente", "success")
    else:
        flash("No se pudo registrar", "error")
    return redirect(url_for("auth.admin_ingresos"))

@auth_bp.route('/admin-dashboard/transacciones/update/<int:id_transaccion>', methods=['GET', 'POST'])
def update_transaccion_view(id_transaccion):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    if request.method == 'POST':
        tipo_transaccion = request.form['tipo_transaccion']
        costo = request.form['costo']
        id_tipo_cambio = request.form['id_tipo_cambio']
        Transaccion.update_transaccion(id_transaccion, tipo_transaccion, costo, id_tipo_cambio)
        return redirect(url_for('auth.admin_ingresos'))

    transaccion = Transaccion.find_by(id_transaccion)
    return render_template('admin/ingresos/transaccion_update.html', transaccion=transaccion)

@auth_bp.route('/admin-dashboard/transacciones/delete/<int:id_transaccion>', methods=['GET'])
def delete_transaccion_view(id_transaccion):
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    Transaccion.delete_transaccion(id_transaccion)
    return redirect(url_for('auth.admin_ingresos'))

@auth_bp.route('/admin-dashboard/transaccion/registrar', methods=['GET'])
def registrar_transaccion_view():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    return render_template('admin/ingresos/create_transaccion.html')

@auth_bp.route('/admin-dashboard/tipocambio/registrar', methods=['GET'])
def registrar_tipo_cambio_view():
    if 'user' not in session:
        print("Usuario no autenticado, redirigiendo al login.")
        return redirect(url_for('auth.login'))  # Redirige al login si no está logueado
    return render_template('admin/ingresos/crear_tipo_cambio.html')
