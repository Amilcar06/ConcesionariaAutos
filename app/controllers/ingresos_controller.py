from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.ingresos_model import TipoCambio, Transaccion
from datetime import datetime
import calendar

ingresos_bp = Blueprint('ingresos', __name__)

@ingresos_bp.route("/ingresos")
def index():
    transacciones = Transaccion.find_all()
    return render_template('ingresos/home.html', transacciones=transacciones)

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

@ingresos_bp.route("/ingresos/dashboard")
def dashboard():
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
    return render_template("ingresos/dashboard.html", header=dash_header, meses=ingresos_mensuales, tipo=ingr_tipo)

@ingresos_bp.route("/tipocambio/register", methods=["POST"])
def tipo_cambio_registrar():
    fecha_str = request.form["fechaTipoCambio"]
    valor_dolar = request.form["valorDolar"]
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")

    tipo_cambio = TipoCambio(fecha_tipo_cambio=fecha, valor_dolar=valor_dolar)
    if tipo_cambio.create():
        flash("Se registró correctamente", "success")
    else:
        flash("No se pudo registrar", "error")
    return redirect(url_for("ingresos.index"))

@ingresos_bp.route("/transacciones/register", methods=["POST"])
def transaccion_register():
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
    return redirect(url_for("ingresos.index"))

@ingresos_bp.route('/transacciones/update/<int:id_transaccion>', methods=['GET', 'POST'])
def update_transaccion_view(id_transaccion):
    if request.method == 'POST':
        tipo_transaccion = request.form['tipo_transaccion']
        costo = request.form['costo']
        id_tipo_cambio = request.form['id_tipo_cambio']
        Transaccion.update_transaccion(id_transaccion, tipo_transaccion, costo, id_tipo_cambio)
        return redirect(url_for('ingresos.index'))

    transaccion = Transaccion.find_by(id_transaccion)
    return render_template('ingresos/transaccion_update.html', transaccion=transaccion)

@ingresos_bp.route('/transacciones/delete/<int:id_transaccion>', methods=['GET'])
def delete_transaccion_view(id_transaccion):
    Transaccion.delete_transaccion(id_transaccion)
    return redirect(url_for('ingresos.index'))

@ingresos_bp.route('/transaccion/registrar', methods=['GET'])
def registrar_transaccion_view():
    return render_template('ingresos/create_transaccion.html')

@ingresos_bp.route('/tipocambio/registrar', methods=['GET'])
def registrar_tipo_cambio_view():
    return render_template('ingresos/crear_tipo_cambio.html')
