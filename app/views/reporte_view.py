from flask import redirect, render_template, url_for
from app.models.reporte_models import Reporte

def reporte_1(reporte):
    return render_template('/admin/reportes/reporte_1.html', reportes=reporte)

def reporte_2(reporte):
    return render_template('/admin/reportes/reporte_2.html', reportes=reporte)

def reporte_3(reporte):
    return render_template('/admin/reportes/reporte_3.html', reportes=reporte)

def reporte_4(reporte):
    return render_template('/admin/reportes/reporte_4.html', reportes=reporte)

def reporte_5(reporte):
    return render_template('/admin/reportes/reporte_5.html', reportes=reporte)