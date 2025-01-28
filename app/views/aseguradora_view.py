from flask import redirect, render_template, url_for

def create():
    return render_template('seguros/pagAseguradora/create_aseguradora.html')

def aseguradoras(aseguradoras):
    return render_template('seguros/pagAseguradora/aseguradoras.html', aseguradoras=aseguradoras)

def aseguradora(aseguradora):
    return render_template('seguros/pagAseguradora/aseguradora.html', aseguradora=aseguradora)

def update_aseguradora(aseguradora=None, error=None):
    return render_template('seguros/pagAseguradora/update_aseguradora.html', aseguradora=aseguradora, error=error)

def delete():
    return redirect(url_for('seguros/aseguradora.aseguradoras'))

def aseguradoras_reporte(aseguradoras):
    return render_template('seguros/pagReportes/aseguradoras_rep.html', aseguradoras=aseguradoras)