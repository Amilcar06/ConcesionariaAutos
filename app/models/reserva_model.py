import cx_Oracle
from datetime import datetime
from database import db as db_connection
class Reserva:
    def __init__(self, id_reserva, id_cliente, id_empleado, fecha_inicio, fecha_fin, contrato=None):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.contrato = contrato
        
    def create(self):
        connection =db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO RESERVA (idReserva, idCliente, idEmpleado, fechaInicio, fechaFin, contrato)
                VALUES (:idReserva, :idCliente, :idEmpleado, :fechaInicio, :fechaFin, :contrato)
            """, {
                'idReserva': self.id_reserva,
                'idCliente': self.id_cliente,
                'idEmpleado': self.id_empleado,
                'fechaInicio': self.fecha_inicio,
                'fechaFin': self.fecha_fin,
                'contrato': self.contrato
            })
            connection.commit()
        except Exception as e:
            print("Error al crear reserva:", e)
            return False
        finally:
            cursor.close()
            connection.close()
            return True

    @staticmethod
    def find_by(id_reserva):
        connection = db_connection()
        reserva = None
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT idReserva, idCliente, idEmpleado, fechaInicio, fechaFin, contrato
                FROM RESERVA
                WHERE idReserva = :idReserva
            """, {'idReserva': id_reserva})

            row = cursor.fetchone()
            reserva = row
        except Exception as e:
            print("Error al leer reserva:", e)
        finally:
            cursor.close()
            connection.close()
        return reserva

    @staticmethod
    def update(reserva):
        connection = db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE RESERVA
                SET idCliente = :idCliente,
                    idEmpleado = :idEmpleado,
                    fechaInicio = :fechaInicio,
                    fechaFin = :fechaFin,
                    contrato = :contrato
                WHERE idReserva = :idReserva
            """, {
                'idCliente': reserva.id_cliente,
                'idEmpleado': reserva.id_empleado,
                'fechaInicio': reserva.fecha_inicio,
                'fechaFin': reserva.fecha_fin,
                'contrato': reserva.contrato,
                'idReserva': reserva.id_reserva
            })
            connection.commit()
        except Exception as e:
            print("Error al actualizar reserva:", e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(id_reserva):
        connection = db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM RESERVA
                WHERE idReserva = :idReserva
            """, {'idReserva': id_reserva})
            connection.commit()
        except Exception as e:
            print("Error al eliminar reserva:", e)
        finally:
            cursor.close()
            connection.close()
