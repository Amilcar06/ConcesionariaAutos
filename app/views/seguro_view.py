from flask import redirect, render_template, url_for
from app.models.vehiculo_models import Vehiculo
from app.models.aseguradora_models import Aseguradora

def create_view():
    vehiculos = Vehiculo.find_all_ids()
    aseguradoras = Aseguradora.find_all_ids()
    return render_template('/admin/seguros/pagSeguro/create_seguro.html', vehiculos=vehiculos, aseguradoras=aseguradoras)

def seguros_view(seguros):
    return render_template('/admin/seguros/pagSeguro/seguros.html', seguros=seguros)

def seguro_view(seguro):
    return render_template('/admin/seguros/pagSeguro/seguro.html', seguro=seguro)

def update_seguro_view(seguro=None, error=None):
    vehiculos = Vehiculo.find_all_ids()
    aseguradoras = Aseguradora.find_all_ids()
    return render_template('/admin/seguros/pagSeguro/update_seguro.html', seguro=seguro, error=error, vehiculos=vehiculos, aseguradoras=aseguradoras)

def delete_view():
    return redirect(url_for('seguro.seguros'))

def seguros_vencidos_view(seguros):
    return render_template('/admin/seguros/pagReportes/seguros_vencidos.html', seguros=seguros)

def seguros_activos_view(seguros):
    return render_template('/admin/seguros/pagReportes/seguros_activos.html', seguros=seguros)