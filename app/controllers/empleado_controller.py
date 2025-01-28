from flask import Blueprint, request, redirect, url_for, flash
from views import auth_view
from app.models.empleado_models import EmpleadoPersona
from datetime import datetime

empleado_persona_bp = Blueprint('empleado_persona', __name__)

@empleado_persona_bp.route('/empleado/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return auth_view.admin_create_empleado()
    
    # Validación de datos
    required_fields = ['nom_empleado', 'ap_paterno_empleado', 'ap_materno_empleado', 'direccion', 'telefono', 'fecha_nac', 'email', 'ci', 'usuario', 'password', 'rol']
    for field in required_fields:
        if field not in request.form or not request.form[field]:
            flash(f'El campo {field.replace("_", " ")} es obligatorio.', 'error')
            return redirect(url_for('empleado_persona.create'))

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
        return redirect(url_for('empleado_persona.empleados'))
    except Exception as ex:
        flash('Ocurrió un error al crear el empleado: ' + str(ex), 'error')
        return redirect(url_for('empleado_persona.create'))

@empleado_persona_bp.route('/empleados', methods=['GET', 'POST'])
def empleados():
    search_query = request.args.get('buscar', '')
    empleados = EmpleadoPersona.search_by_name(search_query) if search_query else EmpleadoPersona.find_all()
    return auth_view.admin_gestion_empleados(empleados)

@empleado_persona_bp.route('/empleados/<int:id>')
def empleado(id):
    empleado = EmpleadoPersona.find_by(id)
    if empleado is None:
        flash('No hay un empleado con ese ID.', 'error')
        return redirect(url_for('empleado_persona.empleados'))
    return auth_view.empleado(empleado=empleado)

@empleado_persona_bp.route('/empleados/<int:id>/update', methods=["GET", "POST"])
def update(id):
    if request.method == "GET":
        empleado = EmpleadoPersona.find_by_empleado(id)
        if empleado is None:
            flash('No hay un empleado con ese ID.', 'error')
            return redirect(url_for('empleado_persona.empleados'))
        return auth_view.admin_update_empleado(empleado=empleado)
    
    # Validación de datos
    email_nuevo = request.form.get('email')
    ci_nuevo = request.form.get('ci')
    if not email_nuevo or not ci_nuevo:
        flash('Email y CI son obligatorios.', 'error')
        return redirect(url_for('empleado_persona.update', id=id))

    EmpleadoPersona.update_empleado(id_empleado=id, email=email_nuevo, ci=ci_nuevo)
    flash("Empleado actualizado correctamente", "success")
    return redirect(url_for('empleado_persona.empleados'))

@empleado_persona_bp.route('/empleados/<int:id>/delete')
def delete_empleado(id):
    EmpleadoPersona.delete_empleado(id)
    flash("Empleado eliminado correctamente", "success")
    return redirect(url_for('empleado_persona.empleados'))