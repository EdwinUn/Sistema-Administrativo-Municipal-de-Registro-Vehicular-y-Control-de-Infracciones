import sys
import os

ruta_raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_raiz)

from database.inicializar_db import crear_tablas

def verificar_entorno():
    """Verifica que la base de datos exista. Si no, la crea."""
    try:
        crear_tablas()
        return True
    except Exception as e:
        print(f"Error crítico al inicializar la base de datos: {e}")
        return False

# Por ahora lo dejamos vacío preparándolo para FastAPI
if __name__ == "__main__":
    verificar_entorno()
    print("Base de datos lista. Esperando a FastAPI...")