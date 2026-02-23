import sys
from PySide6.QtWidgets import QApplication

# Importamos la ventana de login que acabamos de crear
from views.login import VentanaLogin

# Opcional: Importar la inicialización de la base de datos 
# por si quieres asegurarte de que las tablas existan al arrancar
# from database.inicializar_db import crear_tablas

def main():
    # 1. (Opcional) Inicializar base de datos
    # crear_tablas()

    # 2. Crear la instancia de la aplicación PySide6
    # sys.argv permite pasar argumentos de línea de comandos si fuera necesario
    app = QApplication(sys.argv)

    # 3. Instanciar la ventana de Login y mostrarla
    ventana_login = VentanaLogin()
    ventana_login.show()

    # 4. Ejecutar el bucle principal de la aplicación (Event Loop)
    # sys.exit asegura que Python cierre limpiamente cuando se cierre la app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()