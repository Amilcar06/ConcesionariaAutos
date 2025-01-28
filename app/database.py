import os
import mysql.connector
from mysql.connector import Error

def db():
    try:
        # Obtener las variables desde Render (o usar valores locales si no están definidas)
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "12345678")
        db_name = os.getenv("DB_NAME", "concesionaria_Autos")
        db_port = os.getenv("DB_PORT", "3306")  # Por defecto 3306

        # Establecer la conexión
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        
        if db_connection.is_connected():
            print('✅ Conexión exitosa a la base de datos en', db_host)
            return db_connection
    except Error as e:
        print(f'❌ Error de conexión: {e}')
    except Exception as ex:
        print(f'⚠️ Ocurrió un error inesperado: {ex}')
    
    return None
