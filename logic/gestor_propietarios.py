
import sqlite3
from database.conexion import obtener_conexion
from logic.validador import Validador
import logic.catalogos as cat
class GestorPropietarios:
    
    @staticmethod
    def registrar_propietario(propietario):
        """Recibe un objeto Propietario, lo valida y lo guarda en la base de datos."""
        
        valido, msj = Validador.validar_nombre_completo(propietario.nombre_completo)
        if not valido: return False, msj

        valido, msj = Validador.validar_direccion(propietario.direccion)
        if not valido: return False, msj

        # 1. Validar formatos usando nuestra herramienta centralizada
        valido, msj = Validador.validar_curp(propietario.curp)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_telefono(propietario.telefono)
        if not valido: return False, msj

        valido, msj = Validador.validar_estado_licencia(propietario.estado_licencia)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_correo(propietario.correo_electronico)
        if not valido: return False, msj

        valido, msj = Validador.validar_estado_propietario(propietario.estado)
        if not valido: return False, msj
        
        # 2. Guardar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO propietarios (
                    nombres, apellido_paterno, apellido_materno, curp, 
                    calle, numero_exterior, numero_interior, colonia, 
                    codigo_postal, ciudad, estado_provincia, telefono, 
                    correo_electronico, estado_licencia, estado, 
                    id_usuario_registro
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                propietario.nombres, propietario.apellido_paterno, propietario.apellido_materno, 
                propietario.curp, propietario.calle, propietario.numero_exterior, 
                propietario.numero_interior, propietario.colonia, propietario.codigo_postal, 
                propietario.ciudad, propietario.estado_provincia, propietario.telefono, 
                propietario.correo_electronico, propietario.estado_licencia, propietario.estado, 
                propietario.id_usuario_registro
            ))
            conexion.commit()
            return True, "Propietario registrado exitosamente."
            
        except sqlite3.IntegrityError:
            # Si SQLite detecta que la CURP ya existe (restricción UNIQUE), lanza este error[cite: 119, 184].
            return False, "Error: La CURP ingresada ya se encuentra registrada en el sistema."
        except Exception as e:
            return False, f"Error inesperado al registrar propietario: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def modificar_propietario(id_propietario, datos, id_usuario):
        """
        Actualiza los datos permitidos del propietario usando el catálogo oficial.
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # 1. Regla de negocio: Impedir inactivación si tiene vehículos activos
            # CAMBIO: Usamos cat.ESTADOS_PROPIETARIO[1] para referirnos a "Inactivo"
            if datos['estado'] == cat.ESTADOS_PROPIETARIO[1]:
                
                # CAMBIO: Usamos marcador de posición (?) y pasamos cat.ESTADOS_VEHICULO[0] ("Activo")
                cursor.execute(f'''
                    SELECT COUNT(*) FROM vehiculos 
                    WHERE id_propietario = ? AND estado_legal = ?
                ''', (id_propietario, cat.ESTADOS_VEHICULO[0]))
                
                if cursor.fetchone()[0] > 0:
                    return False, f"Error: No se puede cambiar a {cat.ESTADOS_PROPIETARIO[1]} al propietario porque tiene vehículos en estado {cat.ESTADOS_VEHICULO[0]}."

            # 2. Ejecutar la actualización
            cursor.execute('''
                UPDATE propietarios 
                SET calle = ?, numero_exterior = ?, numero_interior = ?, 
                    colonia = ?, codigo_postal = ?, ciudad = ?, 
                    estado_provincia = ?, telefono = ?, correo_electronico = ?, 
                    estado_licencia = ?, estado = ?, id_usuario_actualizacion = ?
                WHERE id_propietario = ?
            ''', (
                datos['calle'], datos['num_ext'], datos['num_int'], datos['colonia'],
                datos['cp'], datos['ciudad'], datos['estado_prov'], datos['telefono'],
                datos['correo'], datos['licencia'], datos['estado'], id_usuario, id_propietario
            ))

            conexion.commit()
            return True, "Datos del propietario actualizados correctamente."
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def buscar_propietario_por_curp(curp):
        """Busca y retorna todos los campos desglosados para llenar el formulario de edición."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('''
                SELECT p.*, u1.nombre_usuario as creador, u2.nombre_usuario as modificador
                FROM propietarios p
                LEFT JOIN usuarios u1 ON p.id_usuario_registro = u1.id_usuario
                LEFT JOIN usuarios u2 ON p.id_usuario_actualizacion = u2.id_usuario
                WHERE p.curp = ?
            ''', (curp,))
            f = cursor.fetchone()
            if f:
                # Mapeamos los resultados a un diccionario (ajusta los índices según tu tabla)
                return True, {
                    "id_propietario": f[0], "nombres": f[1], "apellido_paterno": f[2], "apellido_materno": f[3],
                    "curp": f[4], "calle": f[5], "numero_exterior": f[6], "numero_interior": f[7],
                    "colonia": f[8], "codigo_postal": f[9], "ciudad": f[10], "estado_provincia": f[11],
                    "telefono": f[12], "correo": f[13], "estado_licencia": f[14], "estado": f[15],
                    "creador": f[18] if f[18] else "Sistema", "modificador": f[19] if f[19] else "Sin cambios"
                }
            return False, "No se encontró el propietario."
        finally:
            conexion.close()