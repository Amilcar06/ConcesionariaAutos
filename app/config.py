from models.vehiculo_models import Vehiculo
from collections import defaultdict


def prepair_list():
    vehiculos = Vehiculo.find_all()
    list_vehiculo = []
    for vehiculo in vehiculos:
        list_vehiculo.append({
                        "id_vehiculo":vehiculo.id_vehiculo,
                        "id_estado_vehiculo":vehiculo.id_estado_vehiculo,
                        "id_marca":vehiculo.id_marca,
                        "año":vehiculo.anio,
                        "modelo":vehiculo.modelo,
                        "precio_diario":vehiculo.precio_diario,
                        "precio_dolar":vehiculo.precio_dolar,
                        "caracteristicas":vehiculo.caracteristicas
                    })
    return list_vehiculo
def index_dat(vehicles):
    index = defaultdict(list)
    
    for vehicle in vehicles:
        words = vehicle['modelo'].lower().split()
        for word in words:
            index[word].append(vehicle['id_vehiculo'])
        words = vehicle['caracteristicas'].lower().split(", ")
        for word in words:
                index[word].append(vehicle['id_vehiculo'])
    return index

