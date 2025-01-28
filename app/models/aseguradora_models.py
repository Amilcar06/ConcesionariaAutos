from app.database import db

class Aseguradora:
    @staticmethod
    def create_aseguradora(id_aseguradora, nombre_aseguradora, contacto_aseguradora):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ASEGURADORA (idAseguradora, nombreAseguradora, contactoAseguradora) 
                    VALUES (%(id_aseguradora)s, %(nombre_aseguradora)s, %(contacto_aseguradora)s)
                    """,
                    {
                        'id_aseguradora': id_aseguradora,
                        'nombre_aseguradora': nombre_aseguradora,
                        'contacto_aseguradora': contacto_aseguradora
                    }
                )
                connection.commit()
                print("Aseguradora creada exitosamente")
        except Exception as ex:
            print("Error al crear la aseguradora:", ex)
        finally:
            connection.close()

    @staticmethod
    def find_all():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ASEGURADORA ORDER BY idAseguradora")
                aseguradoras = cursor.fetchall()
                return aseguradoras
        except Exception as ex:
            print("Error al obtener las aseguradoras:", ex)
            return []
        finally:
            connection.close()

    @staticmethod
    def find_by(id):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM ASEGURADORA WHERE idAseguradora = %(id_aseguradora)s",
                    {'id_aseguradora': id}
                )
                aseguradoras = cursor.fetchone()
                return aseguradoras
        except Exception as ex:
            print("Error al buscar la aseguradora:", ex)
            return None
        finally:
            connection.close()

    @staticmethod
    def update_aseguradora(id_aseguradora, nuevo_nombre_aseguradora, nuevo_contacto_aseguradora):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ASEGURADORA 
                    SET nombreAseguradora = %(nuevo_nombre_aseguradora)s, 
                        contactoAseguradora = %(nuevo_contacto_aseguradora)s
                    WHERE idAseguradora = %(id_aseguradora)s
                    """,
                    {
                        'nuevo_nombre_aseguradora': nuevo_nombre_aseguradora,
                        'nuevo_contacto_aseguradora': nuevo_contacto_aseguradora,
                        'id_aseguradora': id_aseguradora
                    }
                )
                connection.commit()
                print("Aseguradora actualizada exitosamente")
        except Exception as ex:
            print("Error al actualizar la aseguradora:", ex)
        finally:
            connection.close()

    @staticmethod
    def delete_aseguradora(id_aseguradora):
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ASEGURADORA WHERE idAseguradora = %(id_aseguradora)s",
                    {'id_aseguradora': id_aseguradora}
                )
                connection.commit()
                print("Aseguradora eliminada exitosamente")
        except Exception as ex:
            print("Error al eliminar la aseguradora:", ex)
        finally:
            connection.close()

    @staticmethod
    def find_all_ids():
        connection = db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT idAseguradora FROM ASEGURADORA")
                aseguradora_ids = cursor.fetchall()
                return [row[0] for row in aseguradora_ids]
        except Exception as ex:
            print("Error al obtener los IDs de las aseguradoras:", ex)
            return []
        finally:
            connection.close()
