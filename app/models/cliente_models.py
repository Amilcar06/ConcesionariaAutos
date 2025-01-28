from database import db
import bcrypt
db_connection = db()

class ClientePersona:

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
    def create_cliente(id_persona, fecha_registro):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO CLIENTE (idPersona, fecha_registro)
                    VALUES (%s, %s)
                    """, (id_persona, fecha_registro)
                )
                id_cliente = cursor.lastrowid  # Obtiene el último ID insertado
                connection.commit()
                return id_cliente
        except Exception as e:
            print("Error al crear cliente:", e)
            return None
        finally:
            connection.close()

    @staticmethod
    def create_usuario(id_cliente, nombreUsuario, contrasena):
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO USUARIO (idCliente, nombreUsuario, contrasena, rolUsuario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (id_cliente, nombreUsuario, hashed_contrasena.decode('utf-8'), 'User')
                )
                connection.commit()
                print("Usuario creado con éxito para el cliente")
        except Exception as e:
            print("Error al crear usuario para el cliente:", e)
        finally:
            connection.close()

    @staticmethod
    def find_all():
        connection = db()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT c.idCliente, p.nombre, p.paterno, p.materno, 
                    p.direccion, p.telefono, p.email, p.fecha_nacimiento, c.fecha_registro
                    FROM CLIENTE c
                    JOIN PERSONA p ON c.idPersona = p.idPersona
                    """
                )
                clientes = cursor.fetchall()
                return clientes
        except Exception as e:
            print("Error al obtener clientes:", e)
            return []
        finally:
            connection.close()

    @staticmethod
    def find_by_id(id_cliente):
        connection = db()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT c.idCliente, p.nombre, p.paterno, p.materno, 
                            p.direccion, p.telefono, p.email, p.fecha_nacimiento, c.fecha_registro
                    FROM CLIENTE c
                    JOIN PERSONA p ON c.idPersona = p.idPersona
                    WHERE c.idCliente = %s
                    """, (id_cliente,)
                )
                cliente = cursor.fetchone()
                return cliente
        except Exception as e:
            print("Error al obtener cliente por ID:", e)
            return None
        finally:
            connection.close()

    @staticmethod
    def update_cliente(id_cliente, nombre, paterno, materno, direccion, telefono, email, fecha_nacimiento, fecha_registro):
        connection = db()
        try:
            with connection.cursor() as cursor:
                # Actualizar los datos en la tabla PERSONA
                cursor.execute(
                    """
                    UPDATE PERSONA
                    SET nombre = %s,
                        paterno = %s,
                        materno = %s,
                        direccion = %s,
                        telefono = %s,
                        email = %s,
                        fecha_nacimiento = %s
                    WHERE idPersona = (
                        SELECT idPersona FROM CLIENTE WHERE idCliente = %s
                    )
                    """, (nombre, paterno, materno, direccion, telefono, email, fecha_nacimiento, id_cliente)
                )

                # Actualizar los datos en la tabla CLIENTE
                cursor.execute(
                    """
                    UPDATE CLIENTE
                    SET fecha_registro = %s
                    WHERE idCliente = %s
                    """, (fecha_registro, id_cliente)
                )
                connection.commit()
        except Exception as e:
            print("Error al actualizar cliente:", e)
        finally:
            connection.close()


    @staticmethod
    def delete_cliente(id_cliente):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM CLIENTE WHERE idCliente = %s", (id_cliente,))
                connection.commit()
        except Exception as ex:
            print("Error al eliminar cliente:", ex)
        finally:
            connection.close()
