import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ruta_raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_raiz)

from database.inicializar_db import crear_tablas

# 1. Aseguramos que la base de datos exista al arrancar
try:
    crear_tablas()
except Exception as e:
    print(f"Error crítico al inicializar la base de datos: {e}")

# 2. Inicializamos la aplicación FastAPI
app = FastAPI(
    title="SAM Vehicular API", 
    description="API para el Sistema Administrativo Municipal Vehicular"
)

# 3. Configuración CORS (Permite que el frontend se comunique con el backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Nota: En producción, aquí pondremos la URL exacta de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# 4. Creamos una ruta de prueba para verificar que el servidor vive
@app.get("/")
def estado_servidor():
    return {
        "sistema": "SAM Vehicular",
        "estado": "En línea",
        "mensaje": "¡El motor FastAPI está funcionando correctamente!"
    }