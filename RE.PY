import bcrypt
import mysql.connector

def rehash_passwords():
    # Conexión a la base de datos
    connection = mysql.connector.connect(
        host="localhost",  # Cambia esto si tu base de datos está en otro servidor
        user="root",  # Cambia por tu nombre de usuario de MySQL
        password="12345678",  # Cambia por tu contraseña de MySQL
        database="concesionaria_Autos"  # Cambia por el nombre de tu base de datos
    )
    cursor = connection.cursor()

    try:
        # Obtén todos los usuarios y sus contraseñas en texto plano
        cursor.execute("SELECT idUsuario, contrasena FROM USUARIO where idUsuario IN (303, 305, 307, 308, 310)")
        users = cursor.fetchall()

        for user in users:
            user_id = user[0]
            plain_password = user[1]
            
            # Hash de la contraseña con bcrypt
            hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

            # Actualiza la contraseña en la base de datos
            cursor.execute("""
                UPDATE USUARIO 
                SET contrasena = %(hashed_password)s 
                WHERE idUsuario = %(user_id)s
            """, {
                "hashed_password": hashed_password.decode('utf-8'), 
                "user_id": user_id
            })

        # Guardar los cambios
        connection.commit()
        print("Contraseñas rehashadas con éxito.")

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        connection.close()

# Llamar a la función para rehashar las contraseñas
rehash_passwords()

"""
{% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <ul class="flashes">
                    {% for category, message in messages %}
                        <li class="text-red-500">{{ message }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
            {% endwith %}
"""

"""
<!-- Asesoría en Compra -->
      <div class="bg-gray-100 p-4 rounded-lg shadow-md">
        <img
          alt="Imagen de un asesor ayudando a un cliente a elegir un auto"
          class="w-full h-32 object-cover mb-4"
          height="200"
          src="{{ url_for('static', filename='recursos/asesoria.jpg') }}"
          width="300"
        />
        <h3 class="text-xl font-bold mb-2">Asesoría en Compra</h3>
        <p>
          Servicios de asesoría para ayudar a los clientes a elegir el vehículo
          adecuado según sus necesidades.
        </p>
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onclick="window.location.href='/contacto'"
        >
          Contactar a un Asesor
        </button>
      </div>
"""

"""
            <nav class="flex space-x-4">
                <a href="/admin-dashboard/aseg" class="inline-block mb-4 px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600">Aseguradoras</a>
                <a href="/admin-dashboard/rep" class="inline-block mb-4 px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600">Reportes</a>
            </nav>
"""