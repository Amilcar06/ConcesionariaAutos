from flask import render_template

def contacto():
    return render_template('contacto.html')

def sobreNostros():
    return render_template('sobreNosotros.html')

def financiamiento():
    return render_template('financiamiento.html')

def servicios():
    return render_template('servicios.html')

def alquileres():
    return render_template('/servicios/alquileres.html')

def home(vehiculos):
    return render_template('index.html', vehiculos=vehiculos)

def inventario(vehiculos):
    return render_template('inventario.html', vehiculos=vehiculos)

def filtro(vehiculos):
    return render_template('inventario.html', vehiculos=vehiculos)

def detalleVehiculo():
    return render_template('/vehiculos/detalleVehiculo.html')


