import mysql.connector
import bcrypt
from app.database import db

class User:
    def __init__(self, username, password, role=None, user_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.user_id = user_id

    @staticmethod
    def validate_user(username, password):
        connection = db()  # Asumiendo que db() devuelve una conexión válida
        try:
            with connection.cursor(dictionary=True) as cursor:
                # Buscar al usuario, uniendo con EMPLEADO o CLIENTE según corresponda
                cursor.execute(
                    """
                    SELECT 
                        u.idUsuario, 
                        u.nombreUsuario, 
                        u.contrasena, 
                        u.rolUsuario,
                        c.idCliente,
                        e.idEmpleado,
                        CONCAT(p.nombre, ' ', p.paterno, ' ', p.materno) AS fullname
                    FROM USUARIO u
                    LEFT JOIN EMPLEADO e ON u.idEmpleado = e.idEmpleado
                    LEFT JOIN CLIENTE c ON u.idCliente = c.idCliente
                    LEFT JOIN PERSONA p ON (e.idPersona = p.idPersona OR c.idPersona = p.idPersona)
                    WHERE u.nombreUsuario = %(username)s
                    """,
                    {'username': username}
                )
                user = cursor.fetchone()  # Recupera el primer resultado como un diccionario

                if user:
                    stored_password = user['contrasena']
                    fullname = user['fullname']
                    role = user['rolUsuario']
                    cliente_id = user.get('idCliente', None)
                    empleado_id = user.get('idEmpleado', None)

                    print(f"Usuario encontrado: {user}")
                    print(f"Contraseña almacenada (encriptada): {stored_password}")

                    # Verificar la contraseña
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        print("Contraseña verificada con éxito")
                        return {
                            "success": True,
                            "message": "Inicio de sesión exitoso",
                            "user_id": user['idUsuario'],
                            "cliente_id": user['idCliente'],
                            "empleado_id": user['idEmpleado'],
                            "role": role,
                            "fullname": fullname,
                        }
                    else:
                        print("Contraseña incorrecta")
                        return {"success": False, "message": "Contraseña incorrecta"}
                else:
                    print(f"No se encontró el usuario con nombre de usuario: {username}")
                    return {"success": False, "message": "Usuario no encontrado"}

        except mysql.connector.Error as e:
            print("Error en la conexión a la base de datos:", e)
            return {"success": False, "message": "Error en la base de datos"}
        except Exception as ex:
            print(f"Error general: {ex}")
            return {"success": False, "message": "Error en la validación del usuario"}
        finally:
            if connection:
                connection.close()


    @staticmethod
    def hash_password(password):
        # Función para generar el hash de la contraseña
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
