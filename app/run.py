from flask import Flask,flash
from controllers import header_controller, auth_controller
from controllers import vehiculo_controller,estado_vehiculo_controller,reserva_controller, ingresos_controller, seguro_controller,aseguradora_controller,routes, empleado_controller, reporte_controller

app = Flask(__name__)

app.secret_key="mi_clave_secreta"

app.register_blueprint(vehiculo_controller.vehiculo_bp)
app.register_blueprint(estado_vehiculo_controller.est_vehiculo_bp)
app.register_blueprint(reserva_controller.reserva_bp)
app.register_blueprint(ingresos_controller.ingresos_bp)
app.register_blueprint(reporte_controller.reporte_bp)
app.register_blueprint(aseguradora_controller.aseguradora_bp)
app.register_blueprint(seguro_controller.seguro_bp)
app.register_blueprint(routes.main)
app.register_blueprint(header_controller.header_bp)
app.register_blueprint(empleado_controller.empleado_persona_bp)
app.register_blueprint(auth_controller.auth_bp)

if __name__ == "__main__":
      app.run(port=5001) 
      app.run(debug=True)


