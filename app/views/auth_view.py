from flask import make_response, render_template

# Vistas de administración
def login_view():
    return render_template('login.html')

def admin_dashboard_view():
    return render_template('/admin/admin_dashboard.html')

# Vistas de gestion de autos
def gestion_vehiculos_view(vehiculos):
    return render_template('/admin/vehiculos/gestion_vehiculos.html', vehiculos=vehiculos)

def creacion_vehiculos_view():
    return render_template('/admin/vehiculos/create_vehiculos.html')

def get_vehiculo_view(vehiculo,estado_vehiculo,marca):
      return render_template('/admin/vehiculos/get_vehiculo.html',vehiculo=vehiculo,estado_vehiculo=estado_vehiculo,marca=marca)

def edit_view(vehiculo):
      return render_template('/admin/vehiculos/edit_vehiculo.html',vehiculo=vehiculo)

def seguimiento_view(seg):
      return render_template('/admin/vehiculos/seguimiento.html',segs=seg)

# Vistas de gestión de empleados
def create_empleado_view():
    return render_template('/admin/empleados/create_empleado.html')

def gestion_empleados_view(empleados):
    return render_template('/admin/empleados/empleados.html', empleados=empleados)

def empleado_view(empleado):
    return render_template('/admin/empleados/empleado.html', empleado=empleado)

def update_empleado_view(empleado):
    return render_template('/admin/empleados/update_empleado.html', empleado=empleado)

#REPORTES

def reporte_1_view(reporte):
    return render_template('/admin/reportes/reporte_1.html', reportes=reporte)

def reporte_2_view(reporte):
    return render_template('/admin/reportes/reporte_2.html', reportes=reporte)

def reporte_3_view(reporte):
    return render_template('/admin/reportes/reporte_3.html', reportes=reporte)

def reporte_4_view(reporte):
    return render_template('/admin/reportes/reporte_4.html', reportes=reporte)

def reporte_5_view(reporte):
    return render_template('/admin/reportes/reporte_5.html', reportes=reporte)

#SEGUROS

def create_seguro_view(vehiculos, aseguradoras):
    return render_template('/admin/seguros/pagSeguro/create_seguro.html', vehiculos=vehiculos, aseguradoras=aseguradoras)

def seguros_view(seguros):
    return render_template('/admin/seguros/pagSeguro/seguros.html', seguros=seguros)

def seguro_view(seguro):
    return render_template('/admin/seguros/pagSeguro/seguro.html', seguro=seguro)

def update_seguro_view(seguro=None, error=None, vehiculos=None, aseguradoras=None):
    return render_template('/admin/seguros/pagSeguro/update_seguro.html', seguro=seguro, error=error, vehiculos=vehiculos, aseguradoras=aseguradoras)

def seguros_vencidos_view(seguros):
    return render_template('/admin/seguros/pagReportes/seguros_vencidos.html', seguros=seguros)

def seguros_activos_view(seguros):
    return render_template('/admin/seguros/pagReportes/seguros_activos.html', seguros=seguros)

#ASEGURADORA

def create_aseguradora_view():
    return render_template('/admin/seguros/pagAseguradora/create_aseguradora.html')

def aseguradoras_view(aseguradoras):
    return render_template('/admin/seguros/pagAseguradora/aseguradoras.html', aseguradoras=aseguradoras)

def aseguradora_view(aseguradora):
    return render_template('/admin/seguros/pagAseguradora/aseguradora.html', aseguradora=aseguradora)

def update_aseguradora_view(aseguradora=None, error=None):
    return render_template('/admin/seguros/pagAseguradora/update_aseguradora.html', aseguradora=aseguradora, error=error)

def aseguradoras_reporte_view(aseguradoras):
    return render_template('/admin/seguros/pagReportes/aseguradoras_rep.html', aseguradoras=aseguradoras)

#CLIENTES

def clientes_view(clientes):
    return render_template('/admin/clientes/clientes.html', clientes=clientes)

def create_cliente_view():
    return render_template('/admin/clientes/create_cliente.html')

def cliente_view(cliente):
    return render_template('/admin/clientes/cliente.html', cliente=cliente)

def update_cliente_view(cliente):
    return render_template('/admin/clientes/update_cliente.html', cliente=cliente)

def cliente_download_view(cliente):
    contenido = (
        f"ID Cliente: {cliente.idCliente}\n"
        f"Nombre: {cliente.nombre}\n"
        f"Apellido Paterno: {cliente.paterno}\n"
        f"Apellido Materno: {cliente.materno}\n"
        f"Dirección: {cliente.direccion}\n"
        f"Teléfono: {cliente.telefono}\n"
        f"Email: {cliente.email}\n"
        f"Fecha de Nacimiento: {cliente.fecha_nacimiento}\n"
        f"Fecha de Registro: {cliente.fecha_registro}\n"
    )
    response = make_response(contenido)
    response.headers["Content-Disposition"] = f"attachment; filename=cliente_{cliente.idCliente}.txt"
    response.headers["Content-Type"] = "text/plain"
    return response
