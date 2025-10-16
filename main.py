from fastapi import FastAPI # type: ignore
from datetime import datetime
from zoneinfo import ZoneInfo
import math

app = FastAPI()

ciudades = {
    "bogota": {"lat": 4.7110, "lon": -74.0055},
    "medellin": {"lat": 6.2442, "lon": -75.5812},
    "cali": {"lat": 3.4372, "lon": -76.5197},
    "cartagena": {"lat": 10.3904, "lon": -75.4794},
}

@app.get("/distance/{ciudad1}/{ciudad2}")
async def get_distance(ciudad1: str, ciudad2: str):
    
    ciudad1 = ciudad1.lower()
    ciudad2 = ciudad2.lower()
    
    if ciudad1 not in ciudades or ciudad2 not in ciudades:
        return {
            "error": "Ciudad no encontrada",
            "ciudades_disponibles": list(ciudades.keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    lat1 = ciudades[ciudad1]["lat"]
    lon1 = ciudades[ciudad1]["lon"]
    lat2 = ciudades[ciudad2]["lat"]
    lon2 = ciudades[ciudad2]["lon"]
    
    # Fórmula de Haversine
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distancia = R * c
    
    return {
        "ciudad_origen": ciudad1.capitalize(),
        "ciudad_destino": ciudad2.capitalize(),
        "distancia_km": round(distancia, 2),
        "tiempo_aproximado_horas": round(distancia / 100, 1),
        "timestamp": datetime.now().isoformat()  # ✅ ISO string
    }