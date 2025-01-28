from app.database import db
from app.models.estado_vehiculo_model import EstadoVehiculo
from app.models.marca import Marca
db_conecction = db()

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

class Vehiculo:
    def __init__(self, id_vehiculo, anio, modelo, precio_diario, precio_dolar, caracteristicas, id_estado_vehiculo, id_marca, imagen_url, combustible, kilometraje):
        self.id_vehiculo = id_vehiculo
        self.anio = anio
        self.modelo = modelo
        self.precio_diario = precio_diario
        self.precio_dolar = precio_dolar
        self.caracteristicas = caracteristicas
        self.id_estado_vehiculo = id_estado_vehiculo
        self.id_marca = id_marca
        self.imagen_url = imagen_url
        self.combustible = combustible
        self.kilometraje = kilometraje

    def create(self):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO VEHICULO (idVehiculo, anio, modelo, precioDiario, precioDolar, caracteristicas, idEstadoVehiculo, idMarca, imagen_url, combustible, kilometraje)
                    VALUES (%(id_vehiculo)s, %(anio)s, %(modelo)s, %(precio_diario)s, %(precio_dolar)s, %(caracteristicas)s, %(id_estado_vehiculo)s, %(id_marca)s, %(imagen_url)s, %(combustible)s, %(kilometraje)s)
                    """,
                    {
                        'id_vehiculo': self.id_vehiculo,
                        'anio': self.anio,
                        'modelo': self.modelo,
                        'precio_diario': self.precio_diario,
                        'precio_dolar': self.precio_dolar,
                        'caracteristicas': self.caracteristicas,
                        'id_estado_vehiculo': self.id_estado_vehiculo,
                        'id_marca': self.id_marca,
                        'imagen_url': self.imagen_url,
                        'combustible': self.combustible,
                        'kilometraje': self.kilometraje
                    }
                )
                connection.commit()
            return True
        except Exception as ex:
            print("Error al crear el vehículo:", ex)
            return None
        finally:
            connection.close()

    @staticmethod
    def find_all():
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM VEHICULO ORDER BY idVehiculo")
        vehiculos = cursor.fetchall()
        list_vehiculo = [Vehiculo(*vh) for vh in vehiculos]
        cursor.close()
        return list_vehiculo

    @staticmethod
    def find_by(id_vehiculo):
        cursor = db_conecction.cursor()
        cursor.execute(
            "SELECT * FROM VEHICULO WHERE idVehiculo = %(id_vehiculo)s",
            {'id_vehiculo': id_vehiculo}
        )
        vehiculo = cursor.fetchone()
        cursor.close()
        return Vehiculo(*vehiculo) if vehiculo else None

    @staticmethod
    def detail(id_vehiculo):
        cursor = db_conecction.cursor()
        cursor.execute(
            """
            SELECT vh.*, ev.nombre_estado AS estado, ev.descripcion, m.nombreMarca, m.descripcion, m.paisMarca
            FROM VEHICULO vh
            INNER JOIN ESTADO_VEHICULO ev ON vh.idEstadoVehiculo = ev.idEstadoVehiculo
            INNER JOIN MARCA m ON vh.idMarca = m.idMarca
            WHERE vh.idVehiculo = %(id_vehiculo)s
            """,
            {'id_vehiculo': id_vehiculo}
        )
        vehiculo_one = cursor.fetchone()
        vehiculo = Vehiculo(*vehiculo_one[:11])
        estado_vehiculo = EstadoVehiculo(vehiculo.id_estado_vehiculo, vehiculo_one[11], vehiculo_one[12])
        marca = Marca(vehiculo.id_marca, vehiculo_one[13], vehiculo_one[14], vehiculo_one[15])
        cursor.close()
        return [vehiculo, estado_vehiculo, marca]

    @staticmethod
    def vehiculo_disponible():
        connection = db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                vh.idVehiculo, vh.anio, vh.modelo, vh.precioDiario, vh.precioDolar, vh.caracteristicas, 
                vh.idEstadoVehiculo, vh.idMarca, vh.imagen_url, vh.combustible, vh.kilometraje,
                ev.idEstadoVehiculo, ev.nombre_estado, ev.descripcion
            FROM VEHICULO vh
            INNER JOIN ESTADO_VEHICULO ev ON vh.idEstadoVehiculo = ev.idEstadoVehiculo
            WHERE LOWER(ev.nombre_estado) LIKE 'disponible'
        """)
        vehiculos = cursor.fetchall()
        list_vh = [
            [Vehiculo(*vh[:11]), EstadoVehiculo(vh[11], vh[12], vh[13])] for vh in vehiculos
        ]
        cursor.close()
        return list_vh

    def update(self, **kwargs):
        connection = db()
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE VEHICULO
                    SET anio = %(anio)s, modelo = %(modelo)s, precioDiario = %(precio_diario)s,
                        precioDolar = %(precio_dolar)s, caracteristicas = %(caracteristicas)s,
                        imagen_url = %(imagen_url)s, combustible = %(combustible)s, kilometraje = %(kilometraje)s
                    WHERE idVehiculo = %(id_vehiculo)s
                    """,
                    self.__dict__
                )
                connection.commit()
        except Exception as ex:
            print("Error al actualizar el vehículo:", ex)
        finally:
            connection.close()

    @staticmethod
    def find_all_ids():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT idVehiculo FROM VEHICULO")
                vehiculo_ids = cursor.fetchall()
                return [row[0] for row in vehiculo_ids]
        except Exception as ex:
            print("Error al obtener los IDs de los vehículos:", ex)
            return []
        finally:
            connection.close()

    @staticmethod
    def seguimient():
        seguimiento = None
        try:
            connection = db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SEGUIMIENTO_VEHICULO")
            lista = []
            for seg in cursor.fetchall():
                lista.append({
                    'id': seg[0],
                    'id_vehiculo': seg[1],
                    'ubicacion_actual': seg[2],
                    'ultima_fecha': seg[3]
                })
            seguimiento = lista
        except Exception as ex:
            print("Error al obtener el seguimiento de vehículos:", ex)
        finally:
            cursor.close()
            connection.close()
        return seguimiento


    @staticmethod
    def delete(id_vehiculo):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM VEHICULO WHERE idVehiculo = %(id_vehiculo)s",
                    {'id_vehiculo': id_vehiculo}
                )
                connection.commit()
        except Exception as ex:
            print("Error al eliminar el vehículo:", ex)
        finally:
            connection.close()

    @staticmethod
    def ver_inventario():
        connection = db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT v.idVehiculo, v.anio, v.modelo, v.precioDolar, m.nombreMarca, 
                   v.imagen_url, v.combustible, v.kilometraje
            FROM VEHICULO v
            INNER JOIN MARCA m ON v.idMarca = m.idMarca
            INNER JOIN ESTADO_VEHICULO e ON v.idEstadoVehiculo = e.idEstadoVehiculo
            WHERE LOWER(e.nombre_estado) LIKE 'disponible'
        """)
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos

    @staticmethod
    def filtrar_vehiculos(marca=None, precio_min=None, precio_max=None, anio=None, kilometraje=None, combustible=None):
        connection = db()
        cursor = connection.cursor()
        query = """
            SELECT v.idVehiculo, v.anio, v.modelo, v.precioDolar, m.nombreMarca AS marca, 
                   v.imagen_url, v.combustible, v.kilometraje, e.nombre_estado AS estado_vehiculo
            FROM VEHICULO v
            INNER JOIN MARCA m ON v.idMarca = m.idMarca
            INNER JOIN ESTADO_VEHICULO e ON e.idEstadoVehiculo = v.idEstadoVehiculo
            WHERE LOWER(e.nombre_estado) LIKE 'disponible'
        """
        params = {}
        if marca:
            query += " AND m.nombreMarca = %(marca)s"
            params['marca'] = marca
        if precio_min is not None and precio_max is not None:
            query += " AND v.precioDolar BETWEEN %(precio_min)s AND %(precio_max)s"
            params['precio_min'] = precio_min
            params['precio_max'] = precio_max
        if anio:
            query += " AND v.anio = %(anio)s"
            params['anio'] = anio
        if kilometraje:
            query += " AND v.kilometraje <= %(kilometraje)s"
            params['kilometraje'] = kilometraje
        if combustible:
            query += " AND v.combustible = %(combustible)s"
            params['combustible'] = combustible
        cursor.execute(query, params)
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos

    @staticmethod
    def ver_vehiculos_dest():
        connection = db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT v.idVehiculo, v.anio, v.modelo, v.precioDolar, m.nombreMarca, v.imagen_url
            FROM VEHICULO v
            INNER JOIN MARCA m ON v.idMarca = m.idMarca
            INNER JOIN ESTADO_VEHICULO e ON v.idEstadoVehiculo = e.idEstadoVehiculo
            WHERE LOWER(e.nombre_estado) LIKE 'disponible'
            ORDER BY v.precioDolar DESC
            LIMIT 3
        """)
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos

    def to_string(self):
        print(self.id_vehiculo,self.anio,self.modelo,self.precio_diario,self.precio_dolar,self.caracteristicas, self.id_estado_vehiculo,self.id_marca, self.imagen_url, self.combustible, self.kilometraje)

    @staticmethod
    def filtrar_por_venta(marca=None, precio_min=None, precio_max=None, anio=None, combustible=None):
        connection = db()
        cursor = connection.cursor()
        query = """
            SELECT v.idVehiculo, v.anio, v.modelo, v.precioDolar, m.nombreMarca, 
                v.imagen_url, v.combustible, v.kilometraje
            FROM VEHICULO v
            INNER JOIN MARCA m ON v.idMarca = m.idMarca
            INNER JOIN ESTADO_VEHICULO e ON v.idEstadoVehiculo = e.idEstadoVehiculo
            WHERE LOWER(e.nombre_estado) LIKE 'disponible'
            AND v.kilometraje = 0
        """
        params = {}
        if marca:
            query += " AND m.nombreMarca = %(marca)s"
            params['marca'] = marca
        if precio_min is not None and precio_max is not None:
            query += " AND v.precioDolar BETWEEN %(precio_min)s AND %(precio_max)s"
            params['precio_min'] = precio_min
            params['precio_max'] = precio_max
        if anio:
            query += " AND v.anio = %(anio)s"
            params['anio'] = anio
        if combustible:
            query += " AND v.combustible = %(combustible)s"
            params['combustible'] = combustible
        query += " ORDER BY v.kilometraje ASC"  # Priorizar los vehículos 0 km
        cursor.execute(query, params)
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos

    @staticmethod
    def filtrar_por_alquiler(marca=None, precio_min=None, precio_max=None, anio=None, kilometraje=None, combustible=None):
        connection = db()
        cursor = connection.cursor()
        query = """
            SELECT v.idVehiculo, v.anio, v.modelo, v.precioDiario, m.nombreMarca, 
                v.imagen_url, v.combustible, v.kilometraje
            FROM VEHICULO v
            INNER JOIN MARCA m ON v.idMarca = m.idMarca
            INNER JOIN ESTADO_VEHICULO e ON v.idEstadoVehiculo = e.idEstadoVehiculo
            WHERE LOWER(e.nombre_estado) LIKE 'disponible'
            AND v.kilometraje > 0
        """
        params = {}
        if marca:
            query += " AND m.nombreMarca = %(marca)s"
            params['marca'] = marca
        if precio_min is not None and precio_max is not None:
            query += " AND v.precioDiario BETWEEN %(precio_min)s AND %(precio_max)s"
            params['precio_min'] = precio_min
            params['precio_max'] = precio_max
        if anio:
            query += " AND v.anio = %(anio)s"
            params['anio'] = anio
        if kilometraje:
            query += " AND v.kilometraje <= %(kilometraje)s"
            params['kilometraje'] = kilometraje
        if combustible:
            query += " AND v.combustible = %(combustible)s"
            params['combustible'] = combustible
        query += " ORDER BY v.kilometraje DESC"  # Priorizar los vehículos con más kilometraje
        cursor.execute(query, params)
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos
