import sqlite3
from database.conexion import obtener_conexion

class GestorReportes:

    @staticmethod
    def ejecutar_consulta(query, parametros=()):
        """
        Función auxiliar para no repetir el código de conexión en cada reporte.
        Retorna: (exito: bool, encabezados: list, filas: list)
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.execute(query, parametros)
            filas = cursor.fetchall()
            
            # Extraemos los nombres de las columnas directamente de la base de datos
            encabezados = [descripcion[0].replace("_", " ").title() for descripcion in cursor.description]
            
            return True, encabezados, filas
        except Exception as e:
            return False, ["Error"], [[str(e)]]
        finally:
            conexion.close()

    # 1. Vehículos con infracciones pendientes [cite: 350]
    @staticmethod
    def reporte_vehiculos_infracciones_pendientes():
        query = '''
            SELECT v.placa, v.vin, v.marca, v.modelo, COUNT(i.folio) as total_multas_pendientes
            FROM vehiculos v
            JOIN infracciones i ON v.vin = i.vin_infractor
            WHERE i.estado = 'Pendiente'
            GROUP BY v.vin
            ORDER BY total_multas_pendientes DESC
        '''
        return GestorReportes.ejecutar_consulta(query)

    # 2. Infracciones por rango de fechas [cite: 351]
    @staticmethod
    def reporte_infracciones_por_fecha(fecha_inicio, fecha_fin):
        query = '''
            SELECT folio, fecha, hora, lugar, tipo_infraccion, monto, estado
            FROM infracciones
            WHERE fecha BETWEEN ? AND ?
            ORDER BY fecha DESC
        '''
        return GestorReportes.ejecutar_consulta(query, (fecha_inicio, fecha_fin))

    # 3. Infracciones emitidas por agente [cite: 353]
    @staticmethod
    def reporte_infracciones_por_agente():
        query = '''
            SELECT a.numero_placa as ID_Oficial, a.nombre_completo, COUNT(i.folio) as multas_emitidas
            FROM agentes a
            LEFT JOIN infracciones i ON a.id_agente = i.id_agente
            GROUP BY a.id_agente
            ORDER BY multas_emitidas DESC
        '''
        return GestorReportes.ejecutar_consulta(query)

    # 4. Vehículos por estado legal [cite: 354]
    @staticmethod
    def reporte_vehiculos_estado_legal():
        query = '''
            SELECT estado_legal, COUNT(vin) as cantidad_vehiculos
            FROM vehiculos
            GROUP BY estado_legal
            ORDER BY cantidad_vehiculos DESC
        '''
        return GestorReportes.ejecutar_consulta(query)

    # 5. Propietarios con múltiples vehículos [cite: 356]
    @staticmethod
    def reporte_propietarios_multiples_vehiculos():
        # Usamos HAVING para filtrar a los que tienen estrictamente más de 1
        query = '''
            SELECT p.curp, p.nombre_completo, COUNT(v.vin) as vehiculos_registrados
            FROM propietarios p
            JOIN vehiculos v ON p.id_propietario = v.id_propietario
            GROUP BY p.id_propietario
            HAVING COUNT(v.vin) > 1
            ORDER BY vehiculos_registrados DESC
        '''
        return GestorReportes.ejecutar_consulta(query)

    # 6. Resumen general de infracciones [cite: 357]
    @staticmethod
    def reporte_resumen_infracciones():
        query = '''
            SELECT estado as Situacion, COUNT(folio) as Total_Multas, SUM(monto) as Dinero_Acumulado
            FROM infracciones
            GROUP BY estado
        '''
        return GestorReportes.ejecutar_consulta(query)