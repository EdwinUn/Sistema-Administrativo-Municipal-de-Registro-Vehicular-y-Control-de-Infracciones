import sqlite3
from database.conexion import obtener_conexion
from logic.auth import Auth # Importamos Auth por si luego ocupamos hashear contraseñas nuevas
import logic.catalogos as cat
class GestorUsuarios:

    @staticmethod
    def obtener_todos_los_usuarios():
        """
        Devuelve la lista completa de usuarios. 
        Por seguridad absoluta, la consulta omite la columna de contraseñas.
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    u.id_usuario, u.nombre_usuario, u.rol, u.estado,
                    u1.nombre_usuario AS creador,
                    u2.nombre_usuario AS modificador
                FROM usuarios u
                LEFT JOIN usuarios u1 ON u.id_usuario_registro = u1.id_usuario
                LEFT JOIN usuarios u2 ON u.id_usuario_actualizacion = u2.id_usuario
                ORDER BY u.id_usuario ASC
            ''')
            usuarios = cursor.fetchall()
            return True, usuarios
        except Exception as e:
            return False, f"Error al obtener la lista de usuarios: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def actualizar_usuario(id_usuario, nuevo_rol, nuevo_estado, id_usuario_modificador):
        # Usamos cat.ROLES_USUARIO[0] en lugar del texto "Administrador"
        if id_usuario == 1 and (nuevo_estado != "Activo" or nuevo_rol != cat.ROLES_USUARIO[0]):
            return False, "Error de Seguridad: No puede alterar el estado ni el rol del Administrador principal."

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                UPDATE usuarios 
                SET rol = ?, estado = ?, id_usuario_actualizacion = ?
                WHERE id_usuario = ?
            ''', (nuevo_rol, nuevo_estado, id_usuario_modificador, id_usuario))
            
            conexion.commit()
            return True, "Los permisos del usuario han sido actualizados exitosamente."
            
        except Exception as e:
            return False, f"Error inesperado al actualizar usuario: {str(e)}"
        finally:
            conexion.close()