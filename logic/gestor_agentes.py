import sqlite3
from database.conexion import obtener_conexion
from logic.validador import Validador
import logic.catalogos as cat

class GestorAgentes:
    
    @staticmethod
    def registrar_agente(agente):
        """
        Registra un nuevo agente de tránsito. 
        El ID interno se genera automáticamente en la base de datos[cite: 159, 160].
        """
        # 1. Validaciones
        valido, msj = Validador.validar_nombre_completo(agente.nombre_completo)
        if not valido: return False, msj

        # Validar que el estado inicial sea válido según el catálogo
        if agente.estado not in cat.ESTADOS_AGENTE:
            return False, "Error: El estado del agente no es válido."

        # Validar que el número de placa oficial no esté vacío
        # CAMBIO APLICADO AQUÍ: usando agente.numero_placa en lugar de numero_identificacion
        if not agente.numero_placa or len(agente.numero_placa.strip()) == 0:
            return False, "Error: El número de placa (identificación oficial) es obligatorio."

        # 2. Guardar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # CAMBIO APLICADO AQUÍ: agente.numero_placa en la tupla de valores
            cursor.execute('''
                INSERT INTO agentes (nombre_completo, numero_identificacion, cargo, estado)
                VALUES (?, ?, ?, ?)
            ''', (agente.nombre_completo, agente.numero_placa, agente.cargo, agente.estado))
            
            conexion.commit()
            return True, "Agente registrado exitosamente."
            
        except sqlite3.IntegrityError:
            # Capturamos la restricción UNIQUE del número de identificación [cite: 161, 166]
            return False, "Error: El número de placa ingresado ya está asignado a otro agente."
        except Exception as e:
            return False, f"Error inesperado al registrar el agente: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def modificar_agente(id_agente, nuevo_cargo, nuevo_estado):
        """
        Modifica únicamente el cargo y el estado de un agente.
        No permite alterar el nombre completo ni el número de identificación oficial.
        """
        # 1. Validaciones
        valido, msj = Validador.validar_id_agente(id_agente)
        if not valido: return False, msj

        if nuevo_estado not in cat.ESTADOS_AGENTE:
            return False, "Error: El estado proporcionado no es válido."

        if not nuevo_cargo or len(nuevo_cargo.strip()) < 3:
            return False, "Error: El cargo proporcionado no es válido."

        # 2. Actualizar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute('''
                UPDATE agentes 
                SET cargo = ?, estado = ?
                WHERE id_agente = ?
            ''', (nuevo_cargo, nuevo_estado, id_agente))

            if cursor.rowcount == 0:
                return False, "Error: No se encontró un agente con el ID especificado."

            conexion.commit()
            return True, "Datos del agente actualizados correctamente."

        except Exception as e:
            return False, f"Error inesperado al modificar el agente: {str(e)}"
        finally:
            conexion.close()
            
    @staticmethod
    def obtener_agentes_para_combo():
        """Devuelve la lista de agentes activos para llenar el formulario de multas."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            # Solo traemos a los activos, porque un agente despedido no puede poner multas
            cursor.execute("SELECT id_agente, numero_placa, nombre_completo FROM agentes WHERE estado = 'Activo'")
            return True, cursor.fetchall()
        except Exception as e:
            return False, []
        finally:
            conexion.close()