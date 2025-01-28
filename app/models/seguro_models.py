from app.database import db

class Seguro:
    @staticmethod
    def create_seguro(id_seguro, id_vehiculo, id_aseguradora, fecha_inicio, fecha_fin, tipo_seguro, costo):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO SEGURO (idSeguro, idVehiculo, idAseguradora, fechaInicio, fechaFin, tipoSeguro, costo) 
                    VALUES (%(id_seguro)s, %(id_vehiculo)s, %(id_aseguradora)s, %(fecha_inicio)s, %(fecha_fin)s, %(tipo_seguro)s, %(costo)s)
                    """,
                    {
                        'id_seguro': id_seguro,
                        'id_vehiculo': id_vehiculo,
                        'id_aseguradora': id_aseguradora,
                        'fecha_inicio': fecha_inicio,
                        'fecha_fin': fecha_fin,
                        'tipo_seguro': tipo_seguro,
                        'costo': costo
                    }
                )
                connection.commit()
                print("Seguro creado exitosamente")
        except Exception as ex:
            print("Error al crear el seguro:", ex)
        finally:
            connection.close()

    @staticmethod
    def find_all():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM SEGURO ORDER BY idSeguro")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()

    @staticmethod
    def find_by(id_seguro):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM SEGURO WHERE idSeguro = %(id_seguro)s",
                    {'id_seguro': id_seguro}
                )
                seguro = cursor.fetchone()
                return seguro
        finally:
            connection.close()

    @staticmethod
    def update_seguro(id_seguro, nuevo_id_vehiculo, nuevo_id_aseguradora, nueva_fecha_inicio, nueva_fecha_fin, nuevo_tipo_seguro, nuevo_costo):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE SEGURO 
                    SET idVehiculo = %(nuevo_id_vehiculo)s,
                        idAseguradora = %(nuevo_id_aseguradora)s,
                        fechaInicio = %(nueva_fecha_inicio)s,
                        fechaFin = %(nueva_fecha_fin)s,
                        tipoSeguro = %(nuevo_tipo_seguro)s,
                        costo = %(nuevo_costo)s
                    WHERE idSeguro = %(id_seguro)s
                    """,
                    {
                        'nuevo_id_vehiculo': nuevo_id_vehiculo,
                        'nuevo_id_aseguradora': nuevo_id_aseguradora,
                        'nueva_fecha_inicio': nueva_fecha_inicio,
                        'nueva_fecha_fin': nueva_fecha_fin,
                        'nuevo_tipo_seguro': nuevo_tipo_seguro,
                        'nuevo_costo': nuevo_costo,
                        'id_seguro': id_seguro
                    }
                )
                connection.commit()
                print("Seguro actualizado exitosamente")
        except Exception as ex:
            print("Error al actualizar el seguro:", ex)
        finally:
            connection.close()

    @staticmethod
    def delete_seguro(id_seguro):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM SEGURO WHERE idSeguro = %(id_seguro)s",
                    {'id_seguro': id_seguro}
                )
                connection.commit()
                print("Seguro eliminado exitosamente")
        except Exception as ex:
            print("Error al eliminar el seguro:", ex)
        finally:
            connection.close()

    @staticmethod
    def seguros_vencidos():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM SEGURO WHERE fechaFin < NOW()")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()
    
    @staticmethod
    def seguros_activos():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM SEGURO WHERE fechaFin > NOW()")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()

    @staticmethod
    def reporte_1():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_1")
                reportes = cursor.fetchall()
                return reportes
        finally:
            connection.close()

    @staticmethod
    def reporte_2():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_2")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()

    @staticmethod
    def reporte_3():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_3")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()

    @staticmethod
    def reporte_4():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_4")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()

    @staticmethod
    def reporte_5():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_5")
                seguros = cursor.fetchall()
                return seguros
        finally:
            connection.close()
