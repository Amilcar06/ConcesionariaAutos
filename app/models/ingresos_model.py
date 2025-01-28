from app.database import db
import random
db_connection = db()

import os
from mysql.connector import pooling

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))  # Usa 3306 por defecto si no está definido
}

try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **db_config
    )
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

def get_connection():
    return connection_pool.get_connection()

class TipoCambio:
    def __init__(self, id_tipo_cambio=None, fecha_tipo_cambio=None, valor_dolar=None):
        self.id = id_tipo_cambio
        self.fecha = fecha_tipo_cambio
        self.valor_dolar = valor_dolar

    @staticmethod
    def query(query, params=None):
        connection = db_connection
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result

    def create(self):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tipo_cambio (fechatipocambio, valordolar)
                    VALUES (%s, %s)
                    """,
                    (self.fecha, self.valor_dolar)
                )
                connection.commit()
            return True
        except Exception as ex:
            print("Error al crear tipo de cambio:", ex)
            connection.rollback()
            return False

    @staticmethod
    def find_all():
        connection = db_connection
        cursor = connection.cursor()
        cursor.execute("SELECT idtipocambio, fechatipocambio, valordolar FROM tipo_cambio")
        lista = [TipoCambio(*row) for row in cursor.fetchall()]
        cursor.close()
        return lista

    @staticmethod
    def find_by(id):
        connection = db_connection
        cursor = connection.cursor()
        cursor.execute("SELECT idtipocambio, fechatipocambio, valordolar FROM tipo_cambio WHERE idtipocambio = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        return TipoCambio(*row) if row else None

    def update(self):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tipo_cambio
                    SET fechatipocambio = %s, valordolar = %s
                    WHERE idtipocambio = %s
                    """,
                    (self.fecha, self.valor_dolar, self.id)
                )
                connection.commit()
            return True
        except Exception as ex:
            print("Error al actualizar tipo de cambio:", ex)
            connection.rollback()
            return False

    @staticmethod
    def delete(id_tipo_cambio):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tipo_cambio WHERE idtipocambio = %s", (id_tipo_cambio,))
                connection.commit()
            return True
        except Exception as ex:
            print("Error al eliminar tipo de cambio:", ex)
            connection.rollback()
            return False


class Transaccion:
    def __init__(self, id=None, id_cliente=None, tipo_transaccion=None, fecha_transaccion=None, costo=None, id_tipo_cambio=None):
        self.id = id
        self.id_cliente = id_cliente
        self.tipo_transaccion = tipo_transaccion
        self.fecha_transaccion = fecha_transaccion
        self.costo = costo
        self.id_tipo_cambio = id_tipo_cambio

    def create(self):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO transaccion (idcliente, tipotransaccion, fechatransaccion, costo, idtipocambio)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (self.id_cliente, self.tipo_transaccion, self.fecha_transaccion, self.costo, self.id_tipo_cambio)
                )
                connection.commit()
            return True
        except Exception as ex:
            print("Error al crear la transacción:", ex)
            connection.rollback()
            return False
        
    @staticmethod
    def find_by(id_transaccion):
        connection = db_connection
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT idtransaccion, idcliente, tipotransaccion, fechatransaccion, costo, idtipocambio
            FROM transaccion
            WHERE idtransaccion = %s
            """,
            (id_transaccion,)
        )
        row = cursor.fetchone()
        cursor.close()
        return Transaccion(*row) if row else None


    @staticmethod
    def delete_transaccion(id_transaccion):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM transaccion WHERE idtransaccion = %s", (id_transaccion,))
                connection.commit()
        except Exception as ex:
            print("Error al eliminar transacción:", ex)
            connection.rollback()

    @staticmethod
    def find_all():
        connection = db()  # Crea una nueva conexión
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM transaccion")
            lista = [Transaccion(*row) for row in cursor.fetchall()]
            return lista
        except Exception as ex:
            print(f"Error al obtener transacciones: {ex}")
            return []
        finally:
            if connection:
                connection.close()  # Cierra la conexión después de usarla

    @staticmethod
    def update_transaccion(id_transaccion, tipo_transaccion, costo, id_tipo_cambio):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE transaccion
                    SET tipotransaccion = %s, costo = %s, idtipocambio = %s
                    WHERE idtransaccion = %s
                    """,
                    (tipo_transaccion, costo, id_tipo_cambio, id_transaccion)
                )
                connection.commit()
        except Exception as ex:
            print("Error al actualizar transacción:", ex)
            connection.rollback()

    @staticmethod
    def query(query, params=None):
        connection = db_connection
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def validar_estado_vehiculo(id_vehiculo):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT idEstadoVehiculo FROM VEHICULO WHERE idVehiculo = %s",
                    (id_vehiculo,)
                )
                return cursor.fetchone()
        except Exception as ex:
            print(f"Error al validar estado del vehículo: {ex}")
            return None
        finally:
            connection.close()

    @staticmethod
    def crear_transaccion(id_cliente, tipo_transaccion, fecha_transaccion, costo, id_tipo_cambio):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO TRANSACCION (idCliente, tipoTransaccion, fechaTransaccion, costo, idTipoCambio)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cliente, tipo_transaccion, fecha_transaccion, costo, id_tipo_cambio)
                )
                connection.commit()
                return cursor.lastrowid
        except Exception as ex:
            print(f"Error al crear la transacción: {ex}")
            connection.rollback()
            return None
        finally:
            connection.close()
    
    @staticmethod
    def actualizar_estado_vehiculo(id_vehiculo, nuevo_estado):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE VEHICULO
                    SET idEstadoVehiculo = %s
                    WHERE idVehiculo = %s
                    """,
                    (nuevo_estado, id_vehiculo)
                )
                connection.commit()
        except Exception as ex:
            print(f"Error al actualizar el estado del vehículo: {ex}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def registrar_relacion_realiza(id_cliente, id_vehiculo, id_transaccion, monto, fecha):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO REALIZA (idCliente, idVehiculo, idTransaccion, monto, fecha)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cliente, id_vehiculo, id_transaccion, monto, fecha)
                )
                connection.commit()
        except Exception as ex:
            print(f"Error al registrar relación en REALIZA: {ex}")
            connection.rollback()
        finally:
            connection.close()

    @staticmethod
    def procesar_compra(id_cliente, id_vehiculo, monto, fecha, tipo_cambio=1):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                # Validar estado del vehículo
                cursor.execute("SELECT idEstadoVehiculo FROM VEHICULO WHERE idVehiculo = %s", (id_vehiculo,))
                estado_vehiculo = cursor.fetchone()
                if not estado_vehiculo or estado_vehiculo[0] != 1:  # 1 = Disponible
                    return {"success": False, "message": "El vehículo no está disponible para la compra."}

                # Crear la transacción
                cursor.execute(
                    """
                    INSERT INTO TRANSACCION (idCliente, tipoTransaccion, fechaTransaccion, costo, idTipoCambio)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cliente, 'Venta', fecha, monto, tipo_cambio)
                )
                id_transaccion = cursor.lastrowid

                # Actualizar estado del vehículo
                cursor.execute(
                    """
                    UPDATE VEHICULO
                    SET idEstadoVehiculo = 4
                    WHERE idVehiculo = %s
                    """,
                    (id_vehiculo,)
                )

                # Registrar relación en REALIZA
                cursor.execute(
                    """
                    INSERT INTO REALIZA (idCliente, idVehiculo, idTransaccion, monto, fecha)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cliente, id_vehiculo, id_transaccion, monto, fecha)
                )

                # Confirmar transacción
                connection.commit()
                return {"success": True, "message": "Compra realizada con éxito."}
        except Exception as ex:
            connection.rollback()
            print(f"Error al procesar la compra: {ex}")
            return {"success": False, "message": "Error al procesar la compra."}
        finally:
            connection.close()

    @staticmethod
    def procesar_alquiler(id_cliente, id_vehiculo, fecha_inicio, fecha_fin, costo, fecha_transaccion):
        connection = get_connection()  # Usa una nueva conexión
        try:
            with connection.cursor() as cursor:
                # Validar que el vehículo esté disponible
                cursor.execute(
                    "SELECT idEstadoVehiculo FROM VEHICULO WHERE idVehiculo = %s",
                    (id_vehiculo,)
                )
                estado_vehiculo = cursor.fetchone()
                if not estado_vehiculo or estado_vehiculo[0] != 1:  # 1 = Disponible
                    return {"success": False, "message": "El vehículo no está disponible para alquiler."}

                # Obtener un empleado disponible
                id_empleado = Transaccion.obtener_empleado_disponible()
                if not id_empleado:
                    return {"success": False, "message": "No hay empleados disponibles para procesar la reserva."}

                # Crear la transacción
                cursor.execute(
                    """
                    INSERT INTO TRANSACCION (idCliente, tipoTransaccion, fechaTransaccion, costo, idTipoCambio)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cliente, "Alquiler", fecha_transaccion, costo, 1)
                )
                id_transaccion = cursor.lastrowid

                # Actualizar el estado del vehículo a 'Alquilado' (idEstadoVehiculo = 3)
                cursor.execute(
                    """
                    UPDATE VEHICULO
                    SET idEstadoVehiculo = 3
                    WHERE idVehiculo = %s
                    """,
                    (id_vehiculo,)
                )

                # Registrar la reserva en la tabla RESERVA
                cursor.execute(
                    """
                    INSERT INTO RESERVA (idCliente, idEmpleado, fechaInicio, fechaFin, contrato)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_cliente, id_empleado, fecha_inicio, fecha_fin, f"R-{id_transaccion}")
                )

                # Confirmar transacción
                connection.commit()
                return {"success": True, "message": "El alquiler se realizó con éxito."}
        except Exception as ex:
            connection.rollback()
            print(f"Error al procesar el alquiler: {ex}")
            return {"success": False, "message": "Error al procesar el alquiler."}
        finally:
            connection.close()  # Cierra la conexión al final


    @staticmethod
    def obtener_empleado_disponible():
        connection = get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                # Obtener todos los empleados disponibles
                cursor.execute("SELECT idEmpleado FROM EMPLEADO")
                empleados = [row['idEmpleado'] for row in cursor.fetchall()]
                
                # Seleccionar un empleado de forma aleatoria si hay empleados disponibles
                if empleados:
                    id_empleado_random = random.choice(empleados)  # Selección aleatoria
                    return id_empleado_random
                else:
                    print("No hay empleados disponibles.")
                    return None
        except Exception as ex:
            print(f"Error al obtener empleado disponible: {ex}")
            return None
        finally:
            connection.close()