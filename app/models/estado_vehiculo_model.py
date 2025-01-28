from app.database import db

class EstadoVehiculo:
    def __init__(self, id_estado_vehiculo, nombre_estado, descripcion) -> None:
        self.id_estado_vehiculo = id_estado_vehiculo
        self.nombre_estado = nombre_estado
        self.descripcion = descripcion

    def create(self):
        try:
            connection = db()
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ESTADO_VEHICULO (IDESTADOVEHICULO, NOMBRE_ESTADO, DESCRIPCION)
                    VALUES (%(IDESTADOVEHICULO)s, %(NOMBRE_ESTADO)s, %(DESCRIPCION)s)
                    """,
                    {
                        "IDESTADOVEHICULO": self.id_estado_vehiculo,
                        "NOMBRE_ESTADO": self.nombre_estado,
                        "DESCRIPCION": self.descripcion,
                    },
                )
                connection.commit()
            return True
        except Exception as ex:
            print(f"Error al crear el estado del vehículo: {ex}")
            return False

    @staticmethod
    def find_by(id):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM ESTADO_VEHICULO
                    WHERE IDESTADOVEHICULO = %(id_estado_vehiculo)s
                    """,
                    {"id_estado_vehiculo": id},
                )
                x1 = cursor.fetchone()
                if x1:
                    estado = EstadoVehiculo(x1[0], x1[1], x1[2])
                    return estado
                else:
                    print(f"No se encontró el estado del vehículo con ID: {id}")
                    return None
        except Exception as ex:
            print(f"Error al buscar el estado del vehículo: {ex}")
            return None
        finally:
            connection.close()

    def update(self, nombre_estado=None, descripcion=None):
        if nombre_estado is not None:
            self.nombre_estado = nombre_estado
        if descripcion is not None:
            self.descripcion = descripcion

        connection = db()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ESTADO_VEHICULO 
                    SET 
                    NOMBRE_ESTADO = %(NOMBRE_ESTADO)s,
                    DESCRIPCION = %(DESCRIPCION)s
                    WHERE IDESTADOVEHICULO = %(ID)s
                    """,
                    {
                        "NOMBRE_ESTADO": self.nombre_estado,
                        "DESCRIPCION": self.descripcion,
                        "ID": self.id_estado_vehiculo,
                    },
                )
                connection.commit()
            return True
        except Exception as ex:
            print(f"Error al actualizar el estado del vehículo: {ex}")
            return False
        finally:
            connection.close()
