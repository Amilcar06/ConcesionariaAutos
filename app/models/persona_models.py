from database import db

class Persona:
    def __init__(self, id=None, nombre=None, paterno=None, materno=None, direccion=None, telefono=None, email=None, fecha_nacimiento=None):
        self.id = id
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento

    @staticmethod
    def get_all():
        connection = db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                idpersona AS id, 
                nombre, 
                paterno, 
                materno, 
                direccion, 
                telefono, 
                email, 
                fecha_nacimiento 
            FROM persona
        """)
        rows = cursor.fetchall()
        personas = [Persona(**row) for row in rows]
        cursor.close()
        connection.close()
        return personas

    @staticmethod
    def get_by_id(id):
        connection = db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                idpersona AS id, 
                nombre, 
                paterno, 
                materno, 
                direccion, 
                telefono, 
                email, 
                fecha_nacimiento 
            FROM persona 
            WHERE idpersona = %s
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row:
            return Persona(**row)
        return None

    def save(self):
        connection = None
        try:
            connection = db()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO persona (nombre, paterno, materno, direccion, telefono, email, fecha_nacimiento) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (self.nombre, self.paterno, self.materno, self.direccion, self.telefono, self.email, self.fecha_nacimiento))
            connection.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print(f"Error al guardar la persona: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                cursor.close()
                connection.close()

    def update(self):
        connection = None
        try:
            connection = db()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE persona 
                SET nombre = %s, 
                    paterno = %s, 
                    materno = %s, 
                    direccion = %s, 
                    telefono = %s, 
                    email = %s, 
                    fecha_nacimiento = %s 
                WHERE idpersona = %s
            """, (self.nombre, self.paterno, self.materno, self.direccion, self.telefono, self.email, self.fecha_nacimiento, self.id))
            connection.commit()
        except Exception as e:
            print(f"Error al actualizar la persona: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete(self):
        connection = None
        try:
            connection = db()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM persona WHERE idpersona = %s", (self.id,))
            connection.commit()
        except Exception as e:
            print(f"Error al eliminar la persona: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                cursor.close()
                connection.close()

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'paterno': self.paterno,
            'materno': self.materno,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d') if self.fecha_nacimiento else None
        }