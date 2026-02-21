import sqlite3
from database.conexion import obtener_conexion
from logic.validador import Validador

class GestorPropietarios:
    
    @staticmethod
    def registrar_propietario(propietario):
        """Recibe un objeto Propietario, lo valida y lo guarda en la base de datos."""
        
        # 1. Validar formatos usando nuestra herramienta centralizada
        valido, msj = Validador.validar_curp(propietario.curp)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_telefono(propietario.telefono)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_correo(propietario.correo_electronico)
        if not valido: return False, msj

        # 2. Guardar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO propietarios (nombre_completo, curp, direccion, telefono, correo_electronico, estado_licencia, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (propietario.nombre_completo, propietario.curp, propietario.direccion, 
                  propietario.telefono, propietario.correo_electronico, propietario.estado_licencia, propietario.estado))
            
            conexion.commit()
            return True, "Propietario registrado exitosamente."
            
        except sqlite3.IntegrityError:
            # Si SQLite detecta que la CURP ya existe, lanza este error automáticamente
            return False, "Error: La CURP ingresada ya se encuentra registrada en el sistema."
        except Exception as e:
            return False, f"Error inesperado al registrar: {str(e)}"
        finally:
            conexion.close()