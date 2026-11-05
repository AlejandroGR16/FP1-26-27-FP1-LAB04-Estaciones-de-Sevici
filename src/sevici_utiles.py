from collections import namedtuple
import math

EstacionSevici = namedtuple("EstacionSevici", 
    "nombre, direccion, latitud, longitud, capacidad, puestos_libres, bicicletas_disponibles")

def selecciona_color(estacion:EstacionSevici) -> str:
    """
    Devuelve el color en que debe pintarse cada estación según su disponibilidad.

    Parámetros:
    estacion: EstacionSevici

    Devuelve:
    str: "green", "orange", "red" o "gray"
    """
    if int(estacion.capacidad) == 0:
        return 'gray'
    color = int(estacion.bicicletas_disponibles) / int(estacion.capacidad)
    if color == 0:
        return 'gray'
    elif color > 0 and color < 1/3:
        return 'red'
    elif color >= 1/3 and color < 2/3:
        return 'orange'
    else:
        return 'green'

def calcula_estadisticas(estaciones: list[EstacionSevici]) -> tuple[int, int, float, int]:
    """
    Calcula estadísticas de las estaciones.
    Parametros:
    estaciones: lista de EstacionSevici
    Devuelve:
    tupla con (total de bicicletas libres, total de capacidad, porcentaje de ocupación, total de estaciones)
    """
    bicis_libres = sum(i.bicicletas_disponibles for i in estaciones)
    cap_total = sum(i.capacidad for i in estaciones)
    porcentaje_ocupacion = (1-bicis_libres/cap_total)*100
    total_estaciones = len(estaciones)
    return (bicis_libres, cap_total, porcentaje_ocupacion, total_estaciones)

def busca_estaciones_direccion(estaciones: list[EstacionSevici], direccion_parcial: str) -> list[EstacionSevici]:
    """
    Busca las estaciones que contengan en su dirección (subcadena, sin distinguir mayúsculas/minúsculas) la dirección parcial dada.    

    Parametros:
    estaciones: lista de EstacionSevici
    direccion_parcial: subcadena a buscar en la dirección de las estaciones

    Devuelve:
    lista de EstacionSevici que cumplen el criterio
    """
    estaciones_direccion = []
    direccion_parcial = direccion_parcial.lower().strip()
    for est in estaciones:
        if direccion_parcial in est.direccion.lower().strip():
            estaciones_direccion.append(est)
    return estaciones_direccion

def busca_estaciones_con_disponibilidad(estaciones:list[EstacionSevici], min_disponibilidad: float = 0.5) -> list[EstacionSevici]:
    """
    Devuelve una lista de EstacionSevici con al menos el porcentaje mínimo de bicicletas disponible
    indicado.

    Parametros:
    estaciones: lista de EstacionSevici
    min_disponibilidad: porcentaje mínimo de bicicletas disponibles (0.0 a 1.0)
    
    Devuelve:
    lista de EstacionSevici
    """
    estaciones_min_disponibilidad = []
    for est in estaciones:
        if est.capacidad > 0 and (est.bicicletas_disponibles / est.capacidad) >= min_disponibilidad:
            estaciones_min_disponibilidad.append(est)
    return estaciones_min_disponibilidad

def calcula_distancia(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos (latitud, longitud).

    Parámetros:
    p1: tupla (latitud, longitud) del primer punto
    p2: tupla (latitud, longitud) del segundo punto

    Devuelve:
    float: distancia euclídea entre los dos puntos
    """
    return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def busca_estacion_mas_cercana(estaciones:list[EstacionSevici], punto:tuple[float, float]) -> EstacionSevici | None:
    """
    Devuelve la estación más cercana al punto dado (latitud, longitud) que tenga al menos una bicicleta disponible.
    
    Parametros:
    estaciones: lista de EstacionSevici
    punto: tupla (latitud, longitud)

    Devuelve:
    EstacionSevici más cercana con al menos una bicicleta disponible, o None si no hay ninguna.
    """
    estacion_cercana = None
    dist_min = None
    for est in estaciones:
        if ((dist_min==None) or (calcula_distancia(punto,(est.longitud,est.latitud)) < dist_min)) and est.bicicletas_disponibles >= 1:
            estacion_cercana = est
            dist_min = (calcula_distancia(punto,(est.longitud,est.latitud)))
    return estacion_cercana

def calcula_ruta(estaciones:list[EstacionSevici], origen:tuple[float, float], destino:tuple[float, float]) -> tuple[EstacionSevici | None, EstacionSevici | None]   :
    """
    Devuelve las estaciones más cercanas al punto de origen y destino dados, que tengan al menos una bicicleta disponible.

    Parametros: 
    estaciones: lista de EstacionSevici
    origen: tupla (latitud, longitud) del punto de origen
    destino: tupla (latitud, longitud) del punto de destino

    Devuelve:
    tupla con (estacion_origen, estacion_destino)
    """
    estacion_origen = busca_estacion_mas_cercana(estaciones, origen)
    estacion_destino = busca_estacion_mas_cercana(estaciones, destino)
    return estacion_origen, estacion_destino