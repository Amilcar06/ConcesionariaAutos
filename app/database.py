import mysql.connector
from mysql.connector import Error

def db():
    try:
        # Establecer la conexión
        db_connection = mysql.connector.connect(
            host="localhost",  # Cambia esto si tu base de datos está en otro servidor
            user="root",  # Cambia por tu nombre de usuario de MySQL
            password="12345678",  # Cambia por tu contraseña de MySQL
            database="concesionaria_Autos"  # Cambia por el nombre de tu base de datos
        )
        
        if db_connection.is_connected():
            print('Conexión exitosa a la base de datos')
            return db_connection
    except Error as e:
        print(f'Error de conexión: {e}')
    except Exception as ex:
        print(f'Ocurrió un error: {ex}')
    return None