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
            cursor.execute('''
                INSERT INTO agentes (nombre_completo, numero_placa, cargo, estado, id_usuario_registro)
                VALUES (?, ?, ?, ?, ?)
            ''', (agente.nombre_completo, agente.numero_placa, agente.cargo, agente.estado, agente.id_usuario_registro))
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
    def modificar_agente(id_agente, nuevo_cargo, nuevo_estado, id_usuario):
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
                SET cargo = ?, estado = ?, id_usuario_actualizacion = ?
                WHERE id_agente = ?
            ''', (nuevo_cargo, nuevo_estado, id_usuario, id_agente))

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
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            # CAMBIO: Usamos marcador de posición y el valor del catálogo
            query = "SELECT id_agente, numero_placa, nombre_completo FROM agentes WHERE estado = ?"
            cursor.execute(query, (cat.ESTADOS_AGENTE[0],)) 
            return True, cursor.fetchall()
        except Exception as e:
            return False, []
        finally:
            conexion.close()
            
    @staticmethod
    def buscar_agente_por_placa(placa):
        """Busca un agente para cargar sus datos en la pestaña de modificación."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('''
                SELECT a.*, u1.nombre_usuario as creador, u2.nombre_usuario as modificador
                FROM agentes a
                LEFT JOIN usuarios u1 ON a.id_usuario_registro = u1.id_usuario
                LEFT JOIN usuarios u2 ON a.id_usuario_actualizacion = u2.id_usuario
                WHERE a.numero_placa = ?
            ''', (placa,))
            row = cursor.fetchone()
            if row:
                return True, {
                    "id_agente": row[0], "numero_placa": row[1], "nombre_completo": row[2],
                    "cargo": row[3], "estado": row[4],
                    "creador": row[6] if row[6] else "Sistema",
                    "modificador": row[7] if row[7] else "Sin cambios"
                }
            return False, "Agente no encontrado."
        finally:
            conexion.close()