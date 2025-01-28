from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from views import seguro_view
from app.models.seguro_models import Seguro
from app.models.vehiculo_models import Vehiculo
from app.models.aseguradora_models import Aseguradora

seguro_bp = Blueprint('seguro', __name__)
seguro_model = Seguro()  # Create an instance of Seguro

@seguro_bp.route('/seg')
def admin_seguros():
    seguros = seguro_model.find_all()
    return seguro_view.seguros_view(seguros)

@seguro_bp.route('/seg/create/seguro', methods=['GET', 'POST'])
def admin_create():

    if request.method == 'GET':
        vehiculos = Vehiculo.find_all_ids()
        aseguradoras = Aseguradora.find_all_ids()
        return seguro_view.create_view(vehiculos, aseguradoras)
    
    id_seguro = request.form['id_seguro']
    id_vehiculo = request.form['id_vehiculo']
    id_aseguradora = request.form['id_aseguradora']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    tipo_seguro = request.form['tipo_seguro']
    costo = request.form['costo']
      
    fecha_inicio_str = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
    fecha_fin_str = datetime.strptime(fecha_fin, '%d-%m-%Y').date()

    seguro_model.create_seguro(id_seguro, id_vehiculo, id_aseguradora, fecha_inicio_str, fecha_fin_str, tipo_seguro, costo)

    return redirect(url_for('seguro.admin_seguros'))


@seguro_bp.route('/seg/update/<int:id>', methods=["GET", "POST"])
def admin_update(id):
    if request.method == "GET":
        seguro = seguro_model.find_by(id)
        vehiculos = Vehiculo.find_all_ids()
        aseguradoras = Aseguradora.find_all_ids()
        if seguro is None:
            return redirect(url_for('seguro.admin_seguros'))
        return seguro_view.update_seguro_view(seguro=seguro, vehiculos=vehiculos, aseguradoras=aseguradoras)
    
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
    seguro_model.update_seguro(id, id_vehiculo, id_aseguradora, fecha_inicio_str, fecha_fin_str, tipo_seguro, costo)
    flash('Seguro actualizado exitosamente!', 'success')
    return redirect(url_for('seguro.admin_seguros'))

@seguro_bp.route('/seg/delete/<int:id>')
def admin_delete_seguro(id):
    seguro = seguro_model.find_by(id)
    if seguro is None:
        flash('No existe un seguro con ese id', 'error')
    else:
        seguro_model.delete_seguro(id)
    return redirect(url_for('seguro.admin_seguros'))

@seguro_bp.route('/seg/<int:id>')
def admin_seguro(id):
    seguro = seguro_model.find_by(id)
    if seguro is None:
        return redirect(url_for('seguro.admin_seguros'))
    return seguro_view.seguro_view(seguro=seguro)

@seguro_bp.route('/rep/vencidos', methods=['GET'])
def admin_seg_vencido():
    seguros = seguro_model.seguros_vencidos()
    return seguro_view.seguros_vencidos_view(seguros)

@seguro_bp.route('/rep/activos', methods=['GET'])
def admin_seg_activo():
    seguros = seguro_model.seguros_activos()
    return seguro_view.seguros_activos_view(seguros)

