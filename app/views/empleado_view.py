from flask import render_template

def create():
    return render_template('/admin/empleados/create_empleado.html')

def empleados(empleados):
    return render_template('/admin/empleados/empleados.html', empleados=empleados)

def empleado(empleado):
    return render_template('/admin/empleados/empleado.html', empleado=empleado)

def update_empleado(empleado):
    return render_template('/admin/empleados/update_empleado.html', empleado=empleado)

