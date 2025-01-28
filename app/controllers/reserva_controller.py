from flask import Blueprint,request,render_template,flash,redirect,url_for
from app.models.reserva_model import Reserva
from datetime import datetime
reserva_bp = Blueprint('reserva',__name__)

@reserva_bp.route('/reserva/create',methods=["GET","POST"])
def create():
    if request.method == "GET":
        return render_template('reserva_form.html')
    id_reserva = request.form["idReserva"]
    id_cliente = request.form["idCliente"]
    id_empleado = request.form["idEmpleado"]
    fecha_inicio_str = request.form["fechaInicio"]
    fecha_fin_str = request.form["fechaFin"]
    contrato = request.form["contrato"]
    
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
    reserva = Reserva(id_reserva=id_reserva,id_cliente=id_cliente,id_empleado=id_empleado,
            fecha_inicio=fecha_inicio,fecha_fin=fecha_fin,contrato=contrato)
    reserva.create()
    flash("se creo la reserva","success")
    return redirect(url_for("est_vehiculo.vehiculo_disponible"))
        