from flask import Blueprint, render_template, request, redirect, url_for
from models.models import Persona


main = Blueprint('main', __name__)

# Ruta principal que muestra la lista de personas en HTML
@main.route('/clientes', methods=['GET'])
def get_personas():
    personas = Persona.get_all()

    return render_template('clientes/index.html', personas=personas)

# Ruta para mostrar el formulario de agregar persona
@main.route('/cliente/add', methods=['GET'])
def add_persona_form():
    return render_template('clientes/add_persona.html')

# Ruta para procesar el formulario de añadir persona
#-------------------------------------
@main.route('/cliente/add', methods=['POST'])
def add_persona():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    paterno = request.form.get('paterno')
    materno = request.form.get('materno')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    fecha_nacimiento = request.form.get('fecha_nacimiento')

    nueva_persona = Persona(
        id=id,
        nombre=nombre,
        paterno=paterno,
        materno=materno,
        direccion=direccion,
        telefono=telefono,
        email=email,
        fecha_nacimiento=fecha_nacimiento
    )
    nueva_persona.save()
    return redirect(url_for('main.get_personas'))


# Ruta para mostrar el formulario de edición con datos de una persona
@main.route('/cliente/edit/<int:id>', methods=['GET'])
def edit_persona_form(id):
    persona_obj = Persona.get_by_id(id)
    return render_template('clientes/edit_persona.html', persona=persona_obj)

# Ruta para procesar el formulario de edición de persona

@main.route('/cliente/edit/<int:id>', methods=['POST'])
def edit_persona(id):
    persona_obj = Persona.get_by_id(id)
    persona_obj.nombre = request.form.get('nombre')
    persona_obj.paterno = request.form.get('paterno')
    persona_obj.materno = request.form.get('materno')
    persona_obj.direccion = request.form.get('direccion')
    persona_obj.telefono = request.form.get('telefono')
    persona_obj.email = request.form.get('email')
    persona_obj.fecha_nacimiento = request.form.get('fecha_nacimiento')
    
    persona_obj.update()
    return redirect(url_for('main.get_personas'))


# Ruta para eliminar una persona y redirigir a la lista
@main.route('/cliente/delete/<int:id>', methods=['GET'])
def delete_persona(id):
    persona_obj = Persona.get_by_id(id)
    if persona_obj:
        persona_obj.delete()
    return redirect(url_for('main.get_personas'))

# Ruta para verificar si un ID ya existe
@main.route('/cliente/verify', methods=['GET'])
def verify_persona_form():
    id = request.args.get('id')
    persona = Persona.get_by_id(id)
    return render_template('clientes/verify_persona.html', persona=persona)

# Ruta para mostrar el formulario de cambio de ID
@main.route('/cliente/change_id/<int:id>', methods=['GET'])
def change_id_form(id):
    persona = Persona.get_by_id(id)
    return render_template('clientes/change_id.html', persona=persona)

# Ruta para procesar el cambio de ID
@main.route('/cliente/change_id/<int:id>', methods=['POST'])
def change_id(id):
    persona = Persona.get_by_id(id)
    new_id = request.form.get('new_id')
    if Persona.get_by_id(new_id):
        return render_template('change_id.html', persona=persona, error="El nuevo ID ya existe.")
    persona.id = new_id
    persona.update()
    return redirect(url_for('main.get_personas'))

@main.route('/cliente/download/<int:id>', methods=['GET'])
def download_persona(id):
    persona = Persona.get_by_id(id)
    if persona:
        # Crear el contenido del archivo
        contenido = (
            f"ID: {persona.id}\n"
            f"Nombre: {persona.nombre}\n"
            f"Apellido Paterno: {persona.paterno}\n"
            f"Apellido Materno: {persona.materno}\n"
            f"Dirección: {persona.direccion}\n"
            f"Teléfono: {persona.telefono}\n"
            f"Email: {persona.email}\n"
            f"Fecha de Nacimiento: {persona.fecha_nacimiento}\n"
        )
        
        # Generar la respuesta de descarga
        response = make_response(contenido)
        response.headers["Content-Disposition"] = f"attachment; filename=persona_{persona.id}.txt"
        response.headers["Content-Type"] = "text/plain"
        return response
    return redirect(url_for('main.get_personas'))
