from app.database import db
import bcrypt
db_conecction = db()

class EmpleadoPersona:
    
    @staticmethod
    def search_by_name(nombre):
        connection = db()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT e.idEmpleado, p.nombre, p.paterno, p.materno, e.email, e.ci, e.comisionES
                FROM EMPLEADO e
                JOIN PERSONA p ON e.idPersona = p.idPersona
                WHERE LOWER(p.nombre) LIKE CONCAT('%', LOWER(%(nombre)s), '%')
                   OR LOWER(p.paterno) LIKE CONCAT('%', LOWER(%(nombre)s), '%')
                   OR LOWER(p.materno) LIKE CONCAT('%', LOWER(%(nombre)s), '%')
                """
                cursor.execute(query, {'nombre': nombre})
                empleados = cursor.fetchall()
            return empleados
        except Exception as e:
            print("Error al buscar empleados:", e)
            return []
        finally:
            connection.close()

    @staticmethod
    def create_persona(nombre, paterno, materno, direccion, telefono, email, fecha_nac):
        connection = db()
        try:
            with connection.cursor() as cursor:
                print("Datos recibidos para crear persona:", nombre, paterno, materno, direccion, telefono, email, fecha_nac)
                
                cursor.execute(
                    """
                    INSERT INTO PERSONA (nombre, paterno, materno, direccion, telefono, email, fecha_nacimiento)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (nombre, paterno, materno, direccion, telefono, email, fecha_nac),
                )
                id_persona = cursor.lastrowid  # Obtiene el último ID insertado
                connection.commit()
                return id_persona
        except Exception as e:
            print("Error al crear persona:", e)
            return None
        finally:
            connection.close()

    @staticmethod
    def create_empleado(id_persona, email, ci, comisionES):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO EMPLEADO (idPersona, email, ci, comisionES)
                    VALUES (%s, %s, %s, %s)
                    """, (id_persona, email, ci, comisionES)
                )
                id_empleado = cursor.lastrowid  # Obtiene el último ID insertado
                connection.commit()
                return id_empleado
        except Exception as e:
            print("Error al crear empleado:", e)
            return None
        finally:
            connection.close()

    @staticmethod
    def create_usuario(id_empleado, nombreUsuario, contrasena, rolUsuario):
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO USUARIO (idEmpleado, nombreUsuario, contrasena, rolUsuario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (id_empleado, nombreUsuario, hashed_contrasena.decode('utf-8'), rolUsuario)
                )
                connection.commit()
                print("Usuario creado con éxito")
        except Exception as e:
            print("Error al crear usuario:", e)
        finally:
            connection.close()
    
    @staticmethod
    def find_all():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM EMPLEADO")
                empleados = cursor.fetchall()
                return empleados
        except Exception as e:
            print("Error al obtener empleados:", e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def find_by(id):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        e.idEmpleado,
                        CONCAT(p.nombre, ' ', p.paterno, ' ', p.materno) AS nombre_completo,
                        p.direccion,
                        p.telefono,
                        p.email,
                        e.ci,
                        e.comisionES,
                        u.rolUsuario AS rol
                    FROM EMPLEADO e
                    JOIN PERSONA p ON e.idPersona = p.idPersona
                    JOIN USUARIO u ON e.idEmpleado = u.idEmpleado
                    WHERE e.idEmpleado = %(id)s
                    """, {"id": id}
                )
                empleado = cursor.fetchone()
            return empleado
        except Exception as e:
            print("Error al obtener detalles del empleado:", e)
            return None
        finally:
            connection.close()

    @staticmethod
    def find_by_empleado(id_empleado):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM EMPLEADO WHERE idEmpleado = %(id_empleado)s",
                    {'id_empleado': id_empleado}
                )
                empleado = cursor.fetchone()
                return empleado
        except Exception as e:
            print("Error al obtener empleado:", e)
            return None
        finally:
            connection.close()

    @staticmethod
    def update_empleado(id_empleado, email, ci, comisionES):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE EMPLEADO
                    SET email = %s, ci = %s, comisionES = %s
                    WHERE idEmpleado = %s
                    """, (email, ci, comisionES, id_empleado)
                )
                connection.commit()
        except Exception as e:
            print("Error al actualizar el empleado:", e)
        finally:
            connection.close()

    @staticmethod
    def delete_empleado(id_empleado):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM EMPLEADO WHERE idEmpleado = %s", (id_empleado,))
                connection.commit()
        except Exception as ex:
            print("Error al eliminar el empleado:", ex)
        finally:
            connection.close()
