from flask import app, render_template, request

@app.route('/transaccion/registrar', methods=['GET', 'POST'])
def registrar_transaccion():
    if request.method == 'POST':
        # Aquí manejarías la lógica para guardar la transacción
        pass
    return render_template('registrar_transaccion.html')