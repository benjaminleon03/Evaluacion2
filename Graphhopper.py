import requests

# ==========================
# CONFIGURACIÓN
# ==========================
API_KEY = "91e8b24f-7c76-4419-9cda-3d31a44ac6d5"  # reemplázala por tu key de Graphhopper
URL_ROUTE = "https://graphhopper.com/api/1/route"
URL_GEOCODE = "https://graphhopper.com/api/1/geocode"

# ==========================
# FUNCIONES
# ==========================

def obtener_coordenadas(nombre):
    """Convierte un nombre de lugar en coordenadas (lat, lon) usando Graphhopper Geocoding API."""
    params = {"q": nombre, "locale": "es", "limit": 1, "key": API_KEY}
    resp = requests.get(URL_GEOCODE, params=params)
    if resp.status_code != 200:
        print(f"❌ Error al obtener coordenadas para {nombre}")
        return None
    data = resp.json()
    if not data["hits"]:
        print(f"❌ No se encontraron resultados para '{nombre}'")
        return None
    punto = data["hits"][0]
    lat, lon = punto["point"]["lat"], punto["point"]["lng"]
    print(f"📍 {nombre} → {lat:.5f}, {lon:.5f}")
    return f"{lat},{lon}"


def obtener_ruta(origen, destino):
    """Obtiene la ruta entre dos coordenadas."""
    params = {
        "point": [origen, destino],
        "vehicle": "car",
        "locale": "es",
        "points_encoded": "false",
        "key": API_KEY
    }
    r = requests.get(URL_ROUTE, params=params)
    if r.status_code != 200:
        print(f"❌ Error al obtener la ruta (código {r.status_code})")
        return
    data = r.json()
    path = data["paths"][0]
    distancia_km = path["distance"] / 1000
    distancia_millas = distancia_km / 1.60934
    tiempo_seg = path["time"] / 1000
    horas = int(tiempo_seg // 3600)
    minutos = int((tiempo_seg % 3600) // 60)

    print("\n==============================================")
    print(f"Ruta desde {origen} hasta {destino}")
    print("==============================================")
    print(f"Distancia total: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"Duración aproximada: {horas} horas {minutos} minutos")
    print("==============================================")
    print("Narrativa del viaje (instrucciones):")
    for paso in path["instructions"]:
        texto = paso.get("text", "")
        dist_km = paso.get("distance", 0) / 1000
        print(f"→ {texto} ({dist_km:.2f} km)")
    print("==============================================\n")


# ==========================
# PROGRAMA PRINCIPAL
# ==========================
print("=== Calculador de Rutas (Graphhopper) ===")
print("Escriba 's' o 'salir' para terminar.\n")

while True:
    origen = input("Ingrese la ubicación de inicio: ").strip()
    if origen.lower() in ["s", "salir"]:
        print("Programa finalizado. ¡Hasta luego!")
        break

    destino = input("Ingrese la ubicación de destino: ").strip()
    if destino.lower() in ["s", "salir"]:
        print("Programa finalizado. ¡Hasta luego!")
        break

    # convertir nombres a coordenadas si hace falta
    if not ("," in origen and "," in destino):
        origen_coords = obtener_coordenadas(origen)
        destino_coords = obtener_coordenadas(destino)
        if origen_coords and destino_coords:
            obtener_ruta(origen_coords, destino_coords)
    else:
        obtener_ruta(origen, destino)