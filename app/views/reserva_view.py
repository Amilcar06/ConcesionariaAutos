from flask import redirect, render_template, url_for

def create():
      return render_template('create_reserva.html');

def reservas(reservas):
      return render_template('reservas.html',reservas=reservas)

def reserva(reserva):
      return render_template('reserva.html',reserva=reserva)

def update_reserva(reserva=None, error=None):
    return render_template('update_reserva.html', reserva=reserva, error=error)

def delete():
      return redirect(url_for('reserva.reservas'))