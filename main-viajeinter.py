import requests
import sys

# Configuración de la API
API_KEY = '5b3ce3597851110001cf62488f23c2a4677a45feb240e70290895a7a'
BASE_URL = 'https://api.openrouteservice.org/v2/directions/'

def obtener_coordenadas(ciudad):
    """Obtiene las coordenadas de una ciudad usando OpenRouteService Geocoding"""
    geocode_url = f"https://api.openrouteservice.org/geocode/search?api_key={API_KEY}&text={ciudad}"
    try:
        response = requests.get(geocode_url)
        data = response.json()
        if data['features']:
            lon, lat = data['features'][0]['geometry']['coordinates']
            return [lon, lat]
        else:
            print(f"No se encontraron coordenadas para {ciudad}")
            return None
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")
        return None

def calcular_ruta(origen, destino, transporte):
    """Calcula la ruta entre dos puntos usando OpenRouteService"""
    coords_origen = obtener_coordenadas(origen)
    coords_destino = obtener_coordenadas(destino)

    if not coords_origen or not coords_destino:
        return None

    # Seleccionar el tipo de transporte
    if transporte == '1':
        profile = 'driving-car'
    elif transporte == '2':
        profile = 'cycling-regular'
    elif transporte == '3':
        profile = 'foot-walking'
    else:
        print("Opción de transporte no válida")
        return None

    params = {
        'api_key': API_KEY,
        'start': f"{coords_origen[0]},{coords_origen[1]}",
        'end': f"{coords_destino[0]},{coords_destino[1]}"
    }

    try:
        response = requests.get(BASE_URL + profile, params=params)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error al calcular la ruta: {e}")
        return None

def formatear_tiempo(segundos):
    """Convierte segundos a formato horas:minutos:segundos"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def km_a_millas(km):
    """Convierte kilómetros a millas"""
    return km * 0.621371

def mostrar_narrativa(origen, destino, distancia_km, duracion, transporte):
    """Muestra la narrativa del viaje"""
    millas = km_a_millas(distancia_km)
    transporte_texto = {
        '1': 'en automóvil',
        '2': 'en bicicleta',
        '3': 'a pie'
    }.get(transporte, 'en automóvil')
    
    print("\n--- Narrativa del Viaje ---")
    print(f"Tu viaje desde {origen} (Chile) hasta {destino} (Argentina) {transporte_texto}:")
    print(f"- Distancia total: {distancia_km:.2f} km ({millas:.2f} millas)")
    print(f"- Duración estimada: {duracion}")
    print("\nRecomendaciones:")
    if transporte == '1':
        print("- Lleva documentos para el cruce fronterizo")
        print("- Revisa el estado de tu vehículo antes de viajar")
    elif transporte == '2':
        print("- Lleva equipo de seguridad y repuestos para bicicleta")
        print("- Verifica los puntos de descanso en la ruta")
    else:
        print("- Lleva calzado adecuado y protección solar")
        print("- Planifica puntos de abastecimiento")

def main():
    print("""
    ******************************************
    *  Calculador de Rutas Chile-Argentina   *
    *  (Presiona 's' para salir en cualquier *
    *  momento)                              *
    ******************************************
    """)

    while True:
        # Solicitar ciudades
        origen = input("\nCiudad de Origen en Chile: ").strip()
        if origen.lower() == 's':
            print("Saliendo del programa...")
            sys.exit(0)

        destino = input("Ciudad de Destino en Argentina: ").strip()
        if destino.lower() == 's':
            print("Saliendo del programa...")
            sys.exit(0)

        # Seleccionar transporte
        print("\nSelecciona medio de transporte:")
        print("1. Automóvil")
        print("2. Bicicleta")
        print("3. A pie")
        transporte = input("Opción (1-3): ").strip()
        if transporte.lower() == 's':
            print("Saliendo del programa...")
            sys.exit(0)

        ruta_data = calcular_ruta(origen, destino, transporte)
        if not ruta_data or 'features' not in ruta_data or not ruta_data['features']:
            print("No se pudo calcular la ruta. Verifique los nombres de las ciudades.")
            continue

        # Extraer información de la ruta
        distancia_km = ruta_data['features'][0]['properties']['segments'][0]['distance'] / 1000
        duracion = formatear_tiempo(ruta_data['features'][0]['properties']['segments'][0]['duration'])
        millas = km_a_millas(distancia_km)

        # Mostrar resultados
        print("\n--- Resultados del Viaje ---")
        print(f"Ruta: {origen} (Chile) -> {destino} (Argentina)")
        print(f"Medio de transporte: {'Automóvil' if transporte == '1' else 'Bicicleta' if transporte == '2' else 'A pie'}")
        print(f"Distancia: {distancia_km:.2f} km ({millas:.2f} millas)")
        print(f"Duración del viaje: {duracion}")

        # Mostrar narrativa
        mostrar_narrativa(origen, destino, distancia_km, duracion, transporte)

if __name__ == "__main__":
    main()