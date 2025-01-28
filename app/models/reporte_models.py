from app.database import db

class Reporte:
    def reporte_1(self):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        m.nombreMarca AS Marca,
                    v.modelo,
                    v.anio AS AÑIO,
                    v.caracteristicas,
                    v.precioDolar AS Precio,
                    ev.nombre_estado AS Estado
                    FROM
                    VEHICULO v
                    JOIN
                    MARCA m ON v.idMarca = m.idMarca
                    JOIN
                    ESTADO_VEHICULO ev ON v.idEstadoVehiculo = ev.idEstadoVehiculo
                    GROUP BY
                        v.modelo, v.anio, v.caracteristicas, 
                    v.precioDolar, m.nombreMarca, ev.nombre_estado
                    ORDER BY
                    v.modelo;
                """)
                reportes = cursor.fetchall()
                return reportes
        finally:
            connection.close()

    def reporte_2(self):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT
                    P.nombre, P.paterno, 
                    P.materno, C.fecha_registro 
                FROM 
                    PERSONA P
                INNER JOIN
                    CLIENTE C ON P.idPersona = C.idPersona;                
                """)
                reportes = cursor.fetchall()
                return reportes
        finally:
            connection.close()

    def reporte_3(self):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_3")
                reportes = cursor.fetchall()
                return reportes
        finally:
            connection.close()

    def reporte_4(self):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reporte_4")
                reportes = cursor.fetchall()
                return reportes
        finally:
            connection.close()

    def reporte_5(self):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        r.nombre AS "Nombre Repuesto",
                        r.descripcion AS "Descripción",
                        SUM(mr.cantidad) AS "Cantidad Total Utilizada",
                        COUNT(DISTINCT v.idVehiculo) AS "Vehículos Involucrados"
                    FROM
                        REPUESTOS r
                    JOIN
                        MANTENIMIENTO_REPUESTOS mr ON r.idRepuestos = mr.idRepuestos
                    JOIN
                        MANTENIMIENTO m ON mr.idMantenimiento = m.idMantenimiento
                    JOIN
                        VEHICULO v ON m.idVehiculo = v.idVehiculo
                    GROUP BY
                        r.nombre, r.descripcion
                    ORDER BY
                        "Cantidad Total Utilizada" DESC;
                """)
                reportes = cursor.fetchall()
                return reportes
        finally:
            connection.close()