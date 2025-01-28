from flask import Blueprint,request,redirect,url_for,flash
from app.models.estado_vehiculo_model import EstadoVehiculo
from app.models.vehiculo_models import Vehiculo
from app.views import estado_vehiculo_views

est_vehiculo_bp = Blueprint('est_vehiculo',__name__)


@est_vehiculo_bp.route("/vehiculo/disponible")
def vehiculo_disponible():
    results = Vehiculo.vehiculo_disponible()
    print(results[0][0].id_vehiculo)
    return estado_vehiculo_views.gestionar_disponibilidad(results)

@est_vehiculo_bp.route("/vehiculo/estado/register",methods=["POST","GET"])
def create_estado_vehiculo():
    if request.method == "GET":
        return estado_vehiculo_views.create()

    id = request.form["id_estado"]
    nombre = request.form["nombre_estado"]
    descripcion = request.form["descripcion"]

    estado_vh = EstadoVehiculo(id_estado_vehiculo=id,nombre_estado=nombre,descripcion=descripcion)
    if estado_vh.create() is True:
        flash("Se registro correctamen","success")
    else:
        flash("Ocurrio un error al registrar","error")
    
    return redirect(url_for("est_vehiculo.vehiculo_disponible"))

@est_vehiculo_bp.route('/vehiculo/<int:id>/edit/estado',methods=["GET","POST"])
def edit(id):
    estado = EstadoVehiculo.find_by(id=id)
    if request.method == "GET":
        return estado_vehiculo_views.edit(estado_vehiculo = estado)

    nombre_estado = request.form["nombre_estado"]
    descripcion = request.form["descripcion"]
    
    res = estado.update(nombre_estado=nombre_estado,descripcion=descripcion)

    if res is True:
        flash(f"Se acutalizo correctamente ",'success')
    else:
        flash("Error: no se pudo actualizar el estado","error")
    return redirect(url_for("est_vehiculo.vehiculo_disponible"))

