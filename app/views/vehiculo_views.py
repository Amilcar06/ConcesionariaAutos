from flask import render_template

def admin_gestion_vehiculos_view(vehiculos):
    return render_template('/admin/vehiculos/gestion_vehiculos.html', vehiculos=vehiculos)

def admin_creacion_vehiculos_view():
    return render_template('/admin/vehiculos/create_vehiculos.html')

def get_vehiculo(vehiculo,estado_vehiculo,marca):
      return render_template('admin/vehiculos/get_vehiculo.html',vehiculo=vehiculo,estado_vehiculo=estado_vehiculo,marca=marca)

def vehiculos(vehiculos):
      return render_template('admin/vehiculos/vehiculos.html',vehiculos=vehiculos)

def edit(vehiculo):
      return render_template('admin/vehiculos/edit_vehiculo.html',vehiculo=vehiculo)

def seguimient(seg):
      return render_template('admin/vehiculos/seguimiento.html',segs=seg)