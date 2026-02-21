import sqlite3
from database.conexion import obtener_conexion
from logic.validador import Validador

class GestorVehiculos:
    
    @staticmethod
    def registrar_vehiculo(vehiculo):
        """Recibe un objeto Vehiculo, verifica sus reglas de negocio y lo guarda."""
        
        # 1. Validaciones estructurales y de formato
        valido, msj = Validador.validar_vin(vehiculo.vin)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_anio_vehiculo(vehiculo.anio)
        if not valido: return False, msj

        # 2. Guardar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # Primero verificamos manualmente que el propietario exista (Regla de negocio)
            cursor.execute("SELECT id_propietario FROM propietarios WHERE id_propietario = ?", (vehiculo.id_propietario,))
            if not cursor.fetchone():
                return False, "Error: El ID del propietario no existe en el sistema."

            cursor.execute('''
                INSERT INTO vehiculos (vin, placa, marca, modelo, anio, color, clase, estado_legal, procedencia, id_propietario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vehiculo.vin, vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio, 
                  vehiculo.color, vehiculo.clase_vehiculo, vehiculo.estado_legal, vehiculo.procedencia, vehiculo.id_propietario))
            
            conexion.commit()
            return True, "Vehículo registrado correctamente."
            
        except sqlite3.IntegrityError as e:
            error_str = str(e).lower()
            if 'vin' in error_str:
                return False, "Error: El VIN ingresado ya está registrado. Es único e inmutable."
            elif 'placa' in error_str:
                return False, "Error: La placa ingresada ya está asignada a otro vehículo."
            else:
                return False, "Error de integridad en la base de datos."
        except Exception as e:
            return False, f"Error inesperado al registrar vehículo: {str(e)}"
        finally:
            conexion.close()