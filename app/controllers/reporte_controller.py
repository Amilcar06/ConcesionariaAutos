from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.views import reporte_view
from app.models.reporte_models import Reporte

reporte_bp = Blueprint('reporte', __name__)
reporte_model = Reporte() 

@reporte_bp.route('/admin-dashboard/reporte/reporte_1')
def reporte_1():
    reporte = reporte_model.reporte_1()
    return reporte_view.reporte_1(reporte)

@reporte_bp.route('/admin-dashboard/reporte/reporte_2')
def reporte_2():
    reporte = reporte_model.reporte_2()
    return reporte_view.reporte_2(reporte)

@reporte_bp.route('/admin-dashboard/reporte/reporte_3')
def reporte_3():
    reporte = reporte_model.reporte_3()
    return reporte_view.reporte_3(reporte)

@reporte_bp.route('/admin-dashboard/reporte/reporte_4')
def reporte_4():
    reporte = reporte_model.reporte_4()
    return reporte_view.reporte_4(reporte)

@reporte_bp.route('/admin-dashboard/reporte/reporte_5')
def reporte_5():
    reporte = reporte_model.reporte_5()
    return reporte_view.reporte_5(reporte)