class Propietario:
    def __init__(self, nombres, apellido_paterno, apellido_materno, curp, 
                 calle, numero_exterior, numero_interior, colonia, codigo_postal, 
                 ciudad, estado_provincia, telefono, correo_electronico, 
                 estado_licencia, estado="Activo", id_propietario=None,
                 id_usuario_registro=None, id_usuario_actualizacion=None):
        
        self.id_propietario = id_propietario 
        
        # Personales
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.curp = curp
        
        # Dirección
        self.calle = calle
        self.numero_exterior = numero_exterior
        self.numero_interior = numero_interior
        self.colonia = colonia
        self.codigo_postal = codigo_postal
        self.ciudad = ciudad
        self.estado_provincia = estado_provincia
        
        # Contacto
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.estado_licencia = estado_licencia
        self.estado = estado

        # Trazabilidad (Auditoría)
        self.id_usuario_registro = id_usuario_registro
        self.id_usuario_actualizacion = id_usuario_actualizacion

    @property
    def nombre_completo(self):
        """Ensambla el nombre completo para mantener compatibilidad con el resto del sistema."""
        ap_mat = self.apellido_materno if self.apellido_materno else ""
        return f"{self.nombres} {self.apellido_paterno} {ap_mat}".strip()

    @property
    def direccion(self):
        """Ensambla la dirección para mantener compatibilidad."""
        num_int = f" Int. {self.numero_interior}" if self.numero_interior else ""
        return f"{self.calle} Ext. {self.numero_exterior}{num_int}, Col. {self.colonia}, CP {self.codigo_postal}, {self.ciudad}, {self.estado_provincia}"

    def __repr__(self):
        return f"<Propietario: {self.nombre_completo} - CURP: {self.curp}>"