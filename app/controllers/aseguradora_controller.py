from flask import Blueprint, request, redirect, url_for
from app.views import aseguradora_view
from app.models.aseguradora_models import Aseguradora

aseguradora_bp = Blueprint('aseguradora', __name__)
aseguradora_model = Aseguradora()  # Crear una instancia de Aseguradora

@aseguradora_bp.route('/aseg')
def aseguradoras():
    aseguradoras = aseguradora_model.find_all()
    return aseguradora_view.aseguradoras(aseguradoras)

@aseguradora_bp.route('/aseg/create/aseguradora', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return aseguradora_view.create()
    id_aseguradora = request.form['id_aseguradora']
    nombre_aseguradora = request.form['nombre_aseguradora']
    contacto_aseguradora = request.form['contacto_aseguradora']

    aseguradora_model.create_aseguradora(id_aseguradora, nombre_aseguradora, contacto_aseguradora)

    return redirect(url_for('aseguradora.aseguradoras'))

@aseguradora_bp.route('/aseg/update/<int:id>', methods=["GET", "POST"])
def update(id):
    if request.method == "GET":
        aseguradora = aseguradora_model.find_by(id)
        if aseguradora is None:
            return "No existe una aseguradora con ese id"
        return aseguradora_view.update_aseguradora(aseguradora=aseguradora)
    id_aseguradora = request.form['id_aseguradora']
    nombre_aseguradora = request.form['nombre_aseguradora']
    contacto_aseguradora = request.form['contacto_aseguradora']

    aseguradora_model.update_aseguradora(id_aseguradora, nombre_aseguradora, contacto_aseguradora)

    return redirect(url_for('aseguradora.aseguradoras'))

@aseguradora_bp.route('/aseg/delete/<int:id>')
def delete_aseguradora(id):
    aseguradora_model.delete_aseguradora(id)
    return aseguradora_view.delete()

@aseguradora_bp.route('/aseg/<int:id>')
def aseguradora(id):
    aseguradora = aseguradora_model.find_by(id)
    if aseguradora is None:
        return "No existe una aseguradora con ese id"
    return aseguradora_view.aseguradora(aseguradora=aseguradora)

@aseguradora_bp.route('/rep')
def aseguradora_rep():
    aseguradoras = aseguradora_model.find_all()
    return aseguradora_view.aseguradoras_reporte(aseguradoras)